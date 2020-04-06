# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 20:31:24 2020

@author: Jarwy
"""

import re;
import time;
import pymongo;
import datetime;
from bs4 import BeautifulSoup;
from ebaysdk.finding import Connection as finding;


Keywords = "ssd 128gb";
entriesPerPage = 25
flag = 0
api = finding(appid ='ChiaWeiH-20200213-PRD-fca7fae46-eb3bd471'
              ,debug=True
              ,config_file= None
             );
              
api_request = {"keywords":Keywords
               ,"outputSelector":"SellerInfo"
               , 'paginationInput': {'entriesPerPage': entriesPerPage,'pageNumber': 1 }
              };

flag = 0

now = datetime.datetime.now()

sched_timer = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute,
                                now.second) + datetime.timedelta(seconds=5)

while (True):
    
    now = datetime.datetime.now()
   
    if sched_timer < now < sched_timer + datetime.timedelta(seconds=1):
        time.sleep(1)
        
        
        # 主程序
        # =============================================================================
        # <Ebay API>
        # =============================================================================
        
        response = api.execute('findItemsByKeywords', api_request);
        soup = BeautifulSoup(response.content, "lxml");
        
        totalentries = int(soup.find("totalentries").text);
        items = soup.find_all("item",limit = None);
        

        
        # =============================================================================
        # <Construct the findings>
        # =============================================================================
        #IDList = []
        DateList = [];
        IDList = [];
        CatList =[];
        TitleList = [];
        PriceList = [];
        SiteList = [];
        SellerList = [];
        

        
        for item in items:
            date = item.starttime.string.lower();
            formateDate = re.sub(r"t"," ",date);
            formateDate = re.sub(r"z","",formateDate);
            formateDate = datetime.datetime.strptime(formateDate, '%Y-%m-%d %H:%M:%S.%f');
            DateList.append(formateDate);
            itemid = item.itemid.string.lower();
            IDList.append(itemid);
            cat = item.categoryname.string.lower();
            CatList.append(cat);
            title = item.title.string.lower().strip();
            TitleList.append(title);
            price = float(item.currentprice.string);
            PriceList.append(price);
            site = item.viewitemurl.string.lower();
            SiteList.append(site);
            seller = item.sellerusername.string.lower();
            SellerList.append(seller);
        
        X = totalentries;
        if(X >=100):
            boundery = 100;
        else:
            boundery = totalentries;
        
   
        
        # =============================================================================
        # <Connect with MongoDB>
        # =============================================================================
        count = 0;
#        myclient = pymongo.MongoClient("mongodb://localhost:27017/");
#        mydb = myclient["EbayTest"];
#        mycol = mydb[Keywords];
#    for i in range(0,100):    
        myclient = pymongo.MongoClient("mongodb+srv://Senior_project:t106360211t106360229@cluster0-y0apq.mongodb.net/test?retryWrites=true&w=majority");
        mydb = myclient["Prices"];
        mycol = mydb["All prices"];
#        myquery = { "Source": "Ebay" };
#        a = mycol.delete_one(myquery);
#        print(a);

     
        
        print("________________________________________________________________");
        presentTime = str(datetime.datetime.now());
        print(presentTime);
        for i in range(0,boundery):
            myquery = { "ID": IDList[i]};
            search = mycol.find(myquery)
            results = [x for x in search] #Decomposite List
            if(results==[]):
                print(i, "Not exist, Inserted!", datetime.datetime.now());
                INFO = { "Date":DateList[i], "Price": PriceList[i], "Product": TitleList[i], "Source": "Ebay", "Site": SiteList[i], "ID":IDList[i]}
                x = mycol.insert_one(INFO);
                count = count+1;
        
        if(count==0):
            print("There is no new product!")
        else:
            print(count, "new product(s) was inserted.")
        print("________________________________________________________________");
        # =============================================================================
        # <Build Dataframe>
        # =============================================================================
#        FullList = [IDList,CatList,TitleList,PriceList,SellerList, SiteList]   
#        df = pd.DataFrame(zip(*FullList), columns=['ID','Catrgory', 'Item Name', 'Price', 'Seller', 'Site']); 

        flag = 1
    else:
        
        if flag == 1:
            
            sched_timer = sched_timer + datetime.timedelta(minutes=10)
            flag = 0
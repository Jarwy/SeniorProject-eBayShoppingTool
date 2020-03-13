# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 04:35:01 2020

@author: Jarwy
"""

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
# Fetch time
now = datetime.datetime.now()

sched_timer = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute,
                                now.second) + datetime.timedelta(seconds=5)

# sched_timer = datetime.datetime(2017,12,13,9,30,10)
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
        
        #input(items[0]);
        
        # =============================================================================
        # <Construct the findings>
        # =============================================================================
        #IDList = []
        IDList = [];
        CatList =[];
        TitleList = [];
        PriceList = [];
        SiteList = [];
        SellerList = [];
        
        for item in items:
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
        
        # 
        #for i in range(0,boundery):
        #    print("____________________________________________________________________________________________________________________________");
        #    print(ItemList[i],"\n");
        #    print(CatList[i],"\n");
        #    print(TitleList[i],"\n");
        #    print(PriceList[i],"\n");
        #    print(SellerList[i],"\n");
        #    print(SiteList[i],"\n");
            
        
        
        
        # =============================================================================
        # <Connect with MongoDB>
        # =============================================================================
        count = 0;
        myclient = pymongo.MongoClient("mongodb://localhost:27017/");
        mydb = myclient["Ebay"];
        mycol = mydb[Keywords];
        print("________________________________________________________________");
        print(datetime.datetime.now());
        for i in range(0,boundery):
        #    print("____________________________________________________________________________________________________________________________");
        #    print(IDList[i],"\n");
        #    print(CatList[i],"\n");
        #    print(TitleList[i],"\n");
        #    print(PriceList[i],"\n");
        #    print(SellerList[i],"\n");
        #    print(SiteList[i],"\n"); 
            myquery = { "ID": IDList[i]};
            search = mycol.find(myquery)
            results = [x for x in search] #Decomposite List
        #    results_id = results[i]["ID"]
#        print(datetime.datetime.now());
            if(results==[]):
                print(i, "Not exist, Inserted!", datetime.datetime.now());
                INFO = { "ID":IDList[i], "Category": CatList[i], "Product Name": TitleList[i], "Price": PriceList[i], "Seller": SellerList[i], "Site": SiteList[i]}
                x = mycol.insert_one(INFO) 
                count = count+1;
        
        if(count==0):
            print("There is no new product!")
        else:
            print(count, "new product(s) was inserted.")
        print("________________________________________________________________");
        # =============================================================================
        # <Build Dataframe>
        # =============================================================================
        #FullList = [IDList,CatList,TitleList,PriceList,SellerList, SiteList]   
        #df = pd.DataFrame(zip(*FullList), columns=['ID','Catrgory', 'Item Name', 'Price', 'Seller', 'Site']); 
                
        
        
        flag = 1
    else:
        
        if flag == 1:
           
            sched_timer = sched_timer + datetime.timedelta(seconds=30)
            flag = 0
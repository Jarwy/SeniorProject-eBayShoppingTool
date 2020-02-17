# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 04:35:01 2020

@author: Jarwy
"""

import time;
import pymongo;
import pandas as pd;
from bs4 import BeautifulSoup;
from ebaysdk.finding import Connection as finding;





Keywords = "ssd 128gb";
entriesPerPage = 25
api = finding(appid ='ChiaWeiH-20200213-PRD-fca7fae46-eb3bd471'
#              ,domain='svcs.sandbox.ebay.com'
              ,debug=True
              ,config_file= None
             );
              


api_request = {"keywords":Keywords
               ,"outputSelector":"SellerInfo"
               , 'paginationInput': {'entriesPerPage': entriesPerPage,'pageNumber': 1 }
              };
  



#response = api.execute('findItemsAdvanced', api_request)
response = api.execute('findCompletedItems', api_request);
time.sleep(5);
soup = BeautifulSoup(response.content, "lxml");

totalentries = int(soup.find("totalentries").text);
items = soup.find_all("item");

#input(items[0]);
DateList = [];
IDList = [];
CatList =[];
TitleList = [];
PriceList = [];
SiteList = [];
SellerList = [];
#ShippingInfoList = [];


for item in items:
    date = item.starttime.string.lower();
    DateList.append(date);
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

# 
for i in range(0,4):
    print("____________________________________________________________________________________________________________________________");
    print(DateList[i],"\n");
    print(IDList[i],"\n");
    print(CatList[i],"\n");
    print(TitleList[i],"\n");
    print(PriceList[i],"\n");
    print(SellerList[i],"\n");
    print(SiteList[i],"\n");
    

FullList = [DateList,IDList,CatList,TitleList,PriceList,SellerList, SiteList];
    
df = pd.DataFrame(zip(*FullList), columns=['Date','ID','Catrgory', 'Item Name', 'Price', 'Seller', 'Site']);  

myclient = pymongo.MongoClient("mongodb://localhost:27017/");
mydb = myclient["Ebay"];
mycol = mydb[Keywords];

for i in range(0,entriesPerPage-1):
    
#    print(CatList[i],"\n");
#    print(TitleList[i],"\n");
#    print(PriceList[i],"\n");
#    print(SellerList[i],"\n");
#    print(SiteList[i],"\n"); 
    INFO = { "Category": CatList[i], "Product Name": TitleList[i], "Price": PriceList[i], "Seller": SellerList[i], "Site": SiteList[i]}
    x = mycol.insert_one(INFO) 
    print(x)
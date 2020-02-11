# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 04:35:01 2020

@author: Jarwy
"""

from ebaysdk.finding import Connection as finding;
from bs4 import BeautifulSoup;
import pandas as pd;


Keywords = input("Search:");
api = finding(appid ='ChiaWeiH-20200213-PRD-fca7fae46-eb3bd471', debug=True, config_file = None);
api_request = {"keywords":Keywords, "outputSelector":"SellerInfo"};

response = api.execute('findItemsByKeywords', api_request)
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

X = totalentries;
if(X >=100):
    boundery = 100;
else:
    boundery = totalentries;

# 
for i in range(0,boundery):
    print("____________________________________________________________________________________________________________________________");
    print(DateList[i],"\n");
    print(IDList[i],"\n");
    print(CatList[i],"\n");
    print(TitleList[i],"\n");
    print(PriceList[i],"\n");
    print(SellerList[i],"\n");
    print(SiteList[i],"\n");
    

FullList = [DateList,IDList,CatList,TitleList,PriceList,SellerList, SiteList]
    
df = pd.DataFrame(zip(*FullList), columns=['Date','ID','Catrgory', 'Item Name', 'Price', 'Seller', 'Site']); 
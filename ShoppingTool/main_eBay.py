# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 02:26:29 2020

@author: Jarwy
"""

import time;
import datetime;
import numpy as np;
import pandas as pd;
import DetailList as DL;
import Source_eBay as Source;


entriesPerPage = 50;
Keywords = "ssd 128gb";
api = Source.API("ChiaWeiH-20200213-PRD-fca7fae46-eb3bd471");
request = Source.Requset(Keywords, entriesPerPage, 1);
responce = Source.Execute(api, "findCompletedItems", request);  #"findItemsByKeywords", "findCompletedItems", "findItemsAdvanced"
totalentries, totalpages, items = Source.Beautify(responce);
print(totalpages);
time.sleep(5);
flag = 0

now = datetime.datetime.now()

sched_timer = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute,
                                now.second) + datetime.timedelta(seconds=5)



while (True):
    
    
    
    now = datetime.datetime.now()
    if sched_timer < now < sched_timer + datetime.timedelta(seconds=1):
        time.sleep(1);
        
        EndDate = []
        for i in range(1, 15):#totalpages+1
            DL.DateList = [];
            DL.IDList = [];
            DL.CatList =[];
            DL.TitleList = [];
            DL.PriceList = [];
            DL.SiteList = [];
            DL.SellerList = [];
            DL.SellingStateList = [];
            DL.StateEncodeList = [];
            print(i);
            request = Source.Requset(Keywords, entriesPerPage, i);
            responce = Source.Execute(api, "findCompletedItems", request);  #"findItemsByKeywords", "findCompletedItems", "findItemsAdvanced"
            totalentries, totalpages, items = Source.Beautify(responce);
            Source.Formate(items);
            if(i == totalpages):
                index = np.mod(totalentries, entriesPerPage);
            else:
                index = entriesPerPage;
            Source.DataBase("mongodb://localhost:27017/", "eBay", Keywords, index, EndDate);
            
        EndDate.sort();
        for i in EndDate:
            Source.MonthAverage("mongodb://localhost:27017/", i, Keywords);
            
#        Source.MonthAverage("mongodb://localhost:27017/", "2020-05", Keywords);
        

        FullList = [DL.IDList,DL.CatList,DL.TitleList,DL.PriceList,DL.SellerList, DL.SiteList]   
        df = pd.DataFrame(zip(*FullList), columns=['ID','Catrgory', 'Item Name', 'Price', 'Seller', 'Site']);
        
               
        flag = 1
    else:
        
        if flag == 1:
            
            sched_timer = sched_timer + datetime.timedelta(seconds=30)
            flag = 0



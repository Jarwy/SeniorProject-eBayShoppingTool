# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 02:26:30 2020

@author: Jarwy
"""

import re;
import time;
import pymongo;
import datetime;
import DetailList as DL;
#import main_eBay as main;
from bs4 import BeautifulSoup;             
from ebaysdk.finding import Connection as finding;


def API(MyID):
    API = finding(appid = MyID
                  ,debug = True
                  ,config_file = None
                  );
    return API;

def Requset(keywords, entriesPerPage, pageNumber):
    Request = {"keywords":keywords
               ,'categoryId' : "175669"
               ,"outputSelector":"SellerInfo"
               , 'paginationInput': {'entriesPerPage': entriesPerPage,'pageNumber': pageNumber}
               };
    return Request;

def Execute(API, mode, request):
    Response = API.execute(mode, request);
    time.sleep(10);
    return Response;

def Beautify(response):
    data =  BeautifulSoup(response.content, "lxml");
    totalentries = int(data.find("totalentries").text);
    totalpages = int(data.find("totalpages").text);
    items = data.find_all("item");
    return totalentries, totalpages, items;

def Formate(items):
    for item in items:
        date = item.endtime.string.lower();
        formateDate = re.sub(r"t"," ",date);
        formateDate = re.sub(r"z","",formateDate);
        formateDate = datetime.datetime.strptime(formateDate, '%Y-%m-%d %H:%M:%S.%f');
        DL.DateList.append(formateDate);
        
        itemid = item.itemid.string.lower();
        DL.IDList.append(itemid);
        
        cat = item.categoryname.string.lower();
        DL.CatList.append(cat);
        
        title = item.title.string.lower().strip();
        DL.TitleList.append(title);
        
        price = float(item.currentprice.string);
        DL.PriceList.append(price);
        
        site = item.viewitemurl.string.lower();
        DL.SiteList.append(site);
        
        seller = item.sellerusername.string.lower();
        DL.SellerList.append(seller);
        
        state = item.sellingstate.string.lower();
        DL.SellingStateList.append(state);
        
        if(state == "active"):
            DL.StateEncodeList.append("0");
        elif(state == "ended"):
            DL.StateEncodeList.append("1");
        elif(state == "endedwithsales"):
            DL.StateEncodeList.append("1");
        else:
            DL.StateEncodeList.append("2");
            
def DataBase(client, DB, keywords, boundary, EndDate):
    count = 0;
    print("________________________________________________________________");
    print(datetime.datetime.now());
    for i in range(0,boundary):
        Title = DL.TitleList[i];
        if (not ('lot' in Title or 'Lot' in Title)):
#            Y = DL.DateList[i].year;
#            M = DL.DateList[i].month;
            YM = str(DL.DateList[i])[0:7];
            if(not (YM in EndDate)):
                EndDate.append(YM);
            myclient = pymongo.MongoClient(client);
            x = "eBay_"+keywords.replace(' ', '_');
            y = YM+"_End";
            mycol = myclient[x][y];
            myquery = { "ID": DL.IDList[i]};
            search = mycol.find(myquery)
            results = [x for x in search] #Decomposite List
            if(results==[]):
                print(i, "Not exist, Inserted!", datetime.datetime.now());
                INFO = { "Date":DL.DateList[i], "Price": DL.PriceList[i], "Product": DL.TitleList[i]
                        ,"Source": "eBay", "Site": DL.SiteList[i], "ID":DL.IDList[i]
                        , "Selling Status":DL.StateEncodeList[i]}
                mycol.insert_one(INFO) 
                count = count+1;
    if(count==0):
        print("There is no new product!")
    else:
        print(count, "new product(s) was inserted.")
        print("________________________________________________________________");
        
def MonthAverage(client, collection, keywords):#collection 2018-10
    totalPrice_1 = 0;
    totalPrice_2 = 0;
    myclient = pymongo.MongoClient(client);
    mycol = myclient["eBay_"+keywords.replace(' ', '_')][collection+"_End"];
    myquery_1 = { "Selling Status": "1"};
    myquery_2 = { "Selling Status": "2"};
    result_1 = list(mycol.find(myquery_1));
    result_2 = list(mycol.find(myquery_2));
    for i in result_1:
        totalPrice_1 = totalPrice_1+i["Price"];
    AveragePrice_1 = totalPrice_1/len(result_1);
    for i in result_2:
        totalPrice_2 = totalPrice_2+i["Price"];
    AveragePrice_2 = totalPrice_2/len(result_2);
    ############################################################################################
    mycol = myclient["eBay_"+keywords.replace(' ', '_')][collection[0:4]+" History Price"]; #2018 History Price
    myquery_1 = {"EndedDate": collection};
    myquery_2 = {"EndedDate": collection};
    search_1 = mycol.find(myquery_1);
    search_2 = mycol.find(myquery_2);
    results_1 = [x for x in search_1];
    results_2 = [x for x in search_2];
    if(results_1==[]):
        INFO = {"EndedDate": collection, "Average Price": AveragePrice_1, "Selling Status": "1"}
        mycol.insert_one(INFO);
    else:
        newvalues = {"$set": { "Average Price": AveragePrice_1}}
        mycol.update_one(myquery_1, newvalues);
    
    if(results_2==[]):
        INFO = {"EndedDate": collection, "Average Price": AveragePrice_2, "Selling Status": "2"}
        mycol.insert_one(INFO);
    else:
        newvalues = {"$set": { "Average Price": AveragePrice_2}}
        mycol.update_one(myquery_2, newvalues);
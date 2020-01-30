# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 00:47:49 2020

@author: Jarwy
"""
import re;
import bs4;
import urllib.request as req;

from pandas.core.frame import DataFrame

##<去標籤函式>##    
def DeleteTag(tag): 
    Newline = re.sub(r"<+[^<>]+>","",tag);
    return(Newline);


# 抓取ebay網頁原始碼 (HTML)
url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313.TR11.TRC1.A0.H0.Xgiant+bike.TRS0&_nkw=giant+bike&_sacat=0&LH_TitleDesc=0&_osacat=0&_odkw=giant"
# 建立一個 Request 物件，附加 Headers 的資訊(模擬一般網路使用者)
request = req.Request(url, headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
})

with req.urlopen(request) as response:
    data = response.read().decode("utf-8");

root = bs4.BeautifulSoup(data, "html.parser");
FormattedXML = root.prettify();
SearchItem = root.title.string;
print(SearchItem);
##############################################################################################
#Split each item one by one
ItemsXML = root.find_all("li",class_="s-item")

##############################################################################################
#Store each title
TitleList = [];
for Item in ItemsXML:
    Title = Item.find_all("h3",class_="s-item__title");
    Title = DeleteTag(str(Title));
    TitleList.append(Title);
##############################################################################################

PriceList = [];
for Item in ItemsXML:
    Price = Item.find_all("span",class_="s-item__price");
    Price = DeleteTag(str(Price));
    PriceList.append(Price);
############################################################################################## 
    
ConditionList = [];
for Item in ItemsXML:
    Condition = Item.find_all("span",class_="SECONDARY_INFO");
    Condition = DeleteTag(str(Condition));
    ConditionList.append(Condition);
##############################################################################################    
    
ShippingInfoList = [];
for Item in ItemsXML:
    ShippingInfo = Item.find_all("span",class_="s-item__shipping s-item__logisticsCost");
    ShippingInfo = DeleteTag(str(ShippingInfo));
    ShippingInfoList.append(ShippingInfo);
############################################################################################## 
ItemsInfo = {"Title" : TitleList,
             "Price" : PriceList,
             "Condition" : ConditionList,
             "Shipping Price" : ShippingInfoList };
data = DataFrame(ItemsInfo);

#SiteList = [];
#for Item in ItemsXML:
#    Site = Item.find("a");
##    Site = Site.get('href');
#    SiteList.append(Site);
##############################################################################################     
    
#ItemsWithTag = root.find_all("h3",class_="s-item__title");
#ItemWithoutTag = [];
#for Item in ItemsWithTag:
##    i = str(Item);
#    i = DeleteTag(str(Item))
#    ItemWithoutTag.append(i);
##    print(Item);
##    print("\n\n");
#    
###############################################################################################
#ItemsPrice = root.find_all("span",class_="s-item__price");
#ItemP = [];
#for price in ItemsPrice:
##    i = str(Item);
##    i = DeleteTag(str(Item))
##    ItemWithoutTag.append(i);
#    print(price);
#    print("\n\n");
#    
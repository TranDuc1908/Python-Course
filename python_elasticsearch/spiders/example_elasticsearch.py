# encoding: utf-8
import scrapy
from scrapy import signals as Signals
from scrapy.xlib.pydispatch import dispatcher as Dispatcher

import re
import json
import datetime 
import requests
# from elasticsearch2 import Elasticsearch

class coreFunction(scrapy.Spider):
    def __init__(self):
        self.host = "localhost"
        self.port = 9200
        self.domain = 'http://localhost:9200/'
        self.headerConfig = {'Content-Type': 'application/json'}

    # convert unicode to string
    def unicodeTrans(self, string):
        return u''.join(string).encode('utf-8').strip()

    # sort 
    def sortASC(self, _dict):
        import operator
        import collections
        sortedDict = sorted(_dict.items(), key=operator.itemgetter(1))
        sorted_dict = collections.OrderedDict(sortedDict)
        return sorted_dict.items()
    
    # check if var is exist
    def isset(self, x):
        try: x
        except NameError: x = False
        return x

    # insert a new document
    def insertOne(self,_dict,_type):
        _data = dict()
        _data["doc"] = _dict
        _data["doc"]["created_at"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        _data = json.dumps(_dict)
        _url = self.domain + "project/" + _type
        try:
            resp = requests.post(_url, data=_data, headers=self.headerConfig)
            resp = resp.json()
            return resp
        except:
            return False
    
    # get all record by type
    def getAll(self, _type, _from=0, _limit=1000):
        url = self.domain + "project/" + _type + "/_search"
        try:
            resp = requests.request("get", url, data=json.dumps({"from": _from,"size": _limit}), headers=self.headerConfig)
            resp = resp.json()
            return resp["hits"]["hits"]
        except:
            return False
        
    # search doc by properties
    def searchByProperties(self, _type="", _dict={}, _dictNot={}, _from=0, _limit=1000):
        qry = dict()
        qry["query"] = {"match":_dict} if bool(_dict) is not False else { "match_all": {} }
        qry.update({"from": _from,"size": _limit})
        url = self.domain + "project/"+_type+"_search"
        qry = json.dumps(qry)
        resp = requests.get(url=url, data= qry, headers=self.headerConfig)
        resp = resp.json()

        try: resp["status"]
        except: resp["status"] = False
        if bool(resp["status"]) is not False and resp["status"] != 200: return {"res":False,"data":resp["error"]}
        else: return {"res":True, "data" : resp["hits"]["hits"]}

    # update doc's properties
    def updateProperties(self, _type, id, _dict):
        _data = dict()
        _data["doc"] = _dict
        _data["doc"]["updated_at"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        _data = json.dumps(_data)
        url = self.domain + "project/"+_type+"/"+id+"/_update"
        resp = requests.post(url=url, data=_data, headers=self.headerConfig)
        return resp


class crawlCategory(coreFunction):
    name = "crawlCategory"
    def start_requests(self):
        self.step_1_urls = "https://vnexpress.net/kinh-doanh"
        yield scrapy.Request(url = self.step_1_urls)

    def parse(self, response):
        for cate in response.xpath("//ul[@class='ul-nav-folder']/li/a"):
            href = cate.xpath("./@href").extract_first()
            title = cate.xpath("./text()").extract_first()
            print((href))
            dataToCreate = {
                "title": title,
                "url": "https://vnexpress.net"+href,
            }
            z = self.insertOne(dataToCreate, "category")
            print(z)


class crawlNews(coreFunction):
    name = "crawlNews"
    
    def __init__(self):
        super(crawlNews, self).__init__()

    def start_requests(self):
        listDoc = self.searchByProperties("category/")
        if listDoc["res"] is True:
            for oneDoc in listDoc["data"]:
                url = oneDoc["_source"]["url"]
                yield scrapy.Request(url, meta={"category_title":oneDoc["_source"]["title"], "category_url":oneDoc["_source"]["url"]})
        else:
            print("===================== error goes here =====================")
            print(listDoc["data"])

    def parse(self, response):
        category_title = response.meta.get("category_title")
        category_url = response.meta.get("category_url")

        path = response.xpath("//div[@id='automation_TV0']//article")
        if path: 
            for oneNews in path:
                elmt_a = oneNews.xpath("./h2/a")
                if(len(elmt_a)>0):
                    href = elmt_a.xpath("./@href").extract_first()
                    title = elmt_a.xpath("./text()").extract_first()
                    yield scrapy.Request(
                        href, 
                        callback=self.all_detail_parse,  
                        method="get", 
                        meta={
                        "category_title":category_title, 
                        "category_url":category_url,
                        "detail_url":href,
                        "detail_title":title
                        }
                    )
        
        next_page = response.xpath('//a[contains(@class, "next-page")]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse,  method="get", meta={"category_title":category_title, "category_url":category_url})
        else: print("=========== no next page ==========")

    def all_detail_parse(self, response):
        category_title = response.meta.get("category_title")
        category_url = response.meta.get("category_url")
        detail_url = response.meta.get("detail_url")

        _date = response.xpath(".//span[contains(@class, 'date')]/text()").extract_first()
        _date = ( self.unicodeTrans(_date).split())
        _date = str(_date[2].rstrip(',')) +" "+ str(_date[3])+":00"
        _title = response.xpath("//meta[@property='og:title']/@content").extract_first()
        _intro = response.xpath("//meta[@property='og:description']/@content").extract_first()
        author = response.xpath(".//article[@class='fck_detail ']/p[@style='text-align:right;']/strong/text() | //p[@style='text-align:right;']/em/text()").extract_first()
        _content = response.xpath(".//article[contains(@class, 'fck_detail')]/p//text() | //div[@class='desc_cation']/p//text()").extract()

        newItem = {
            "intro":  _intro,
            "published_at":_date,
            "content":_content,
            "author":author,
            "url":detail_url,
            "url":detail_url,
            "title": _title,
            "category_title":category_title,
            "category_url":category_url
        }
        ins= self.insertOne(newItem, "news")
        print(ins)

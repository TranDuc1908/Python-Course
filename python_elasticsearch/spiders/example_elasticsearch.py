# encoding: utf-8
import scrapy
from scrapy import signals as Signals
from scrapy.xlib.pydispatch import dispatcher as Dispatcher

import json
import datetime 
import requests
from python_elasticsearch.coreFunction.coreDatabase import CoreDatabase
from python_elasticsearch.coreFunction.coreHelper import CoreHelper


class crawlCategory(scrapy.Spider):
    def __init__(self):
        self.coreDatabase = CoreDatabase()
        
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
            z = self.coreDatabase.insertOne(dataToCreate, "category")
            print(z)


class crawlNews(scrapy.Spider):
    name = "crawlNews"
    
    def __init__(self):
        self.coreDatabase = CoreDatabase()
        self.coreHelper = CoreHelper()
        
    def start_requests(self):
        listDoc = self.coreDatabase.getAllDocument("category")
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
        _date = ( self.coreHelper.unicodeTrans(_date).split())
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
        ins= self.coreDatabase.insertOne(newItem, "news")
        print(ins)

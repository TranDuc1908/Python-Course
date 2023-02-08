# encoding: utf-8

import scrapy
from tutorial.modelCustom.category.category import Category as Category
from tutorial.modelCustom.aa_core.core import Core as Core

class crawlParentCate(scrapy.Spider):
    name = "crawlParentCate"
    start_urls = ["https://vnexpress.net/"]
    def parse(self, response):
        clsCategories = Category()
        clsCore = Core()
        print("=====================================================")
        i=0
        while i < len(response.xpath("//ul[@class='parent']//li/a")):
            i += 1
            if i < 3: 
                continue
            if i==5: break

            title = response.xpath("//ul[@class='parent']//li["+str(i)+"]/a/text()").extract()
            title = clsCore.unicodeTrans(title)
            if title == "Góc nhìn" or title == "Tất cả" or title == "Video": continue
            href = response.xpath("//ul[@class='parent']//li["+str(i)+"]/a/@href").extract()
            href = clsCore.unicodeTrans(href)
            z = clsCategories.insertOne(({"title":title}, {"url":href}))
            print(title)

# ===============================================

class crawlChildCate(scrapy.Spider):
    name = "crawlChildCate"
    def start_requests(self):
        clsCategories = Category()
        clsCore = Core()
        listCate = clsCategories.getAll(" order by id asc")
        url = 'https://vnexpress.net'

        if listCate is not None:
            for oneItem in listCate:
                cateUrl = url+oneItem["url"]
                yield scrapy.Request(cateUrl, self.parse(parent_id=oneItem["id"]) )
                break

    def parse(self, response, parent_id):
        clsCategories = Category()
        clsCore = Core()
        print("=====================================================")
        print(parent_id)
        return True
        for elm in response.xpath("//ul[@class='ul-nav-folder']//li/a"):
            title = elm.xpath('.text()').extract()
            title = clsCore.unicodeTrans(title)

            href = elm.xpath('@href').extract()
            href = clsCore.unicodeTrans(href)
            
            z = clsCategories.insertOne(({"title":title}, {"url":href}, {"parent_id":parent_id}))
            print(z)

# ===============================================

class MySpider(scrapy.Spider):
    name = "my_spider"
    def __init__(self):
        clsCategories = Category()
        listCates = clsCategories.getAll(" order by id asc")
        res = []
        for cate in listCates:
            res.append('https://vnexpress.net'+cate["url"])
        self.listUrl = res

    def start_requests(self):
        clsCategories = Category()
        listCates = clsCategories.getAll(" order by id asc")
        for oneItem in listCates:
            yield scrapy.Request(
                'https://vnexpress.net'+oneItem["url"], 
                self.parse(parent_id=oneItem["id"]),
                headers={"User-Agent": "My UserAgent"},
                meta={"proxy": "http://45.119.82.101:3333"}
            )
        
    def parse(self, response, parent_id):
        print("=====================================================")
        print(parent_id)
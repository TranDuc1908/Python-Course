# encoding: utf-8

import scrapy
import json
import unicodedata
from ftfy import fix_encoding
from tutorial.modelCustom.category.category import Category as Category
from tutorial.modelCustom.aa_core.core import Core as Core

class QuotesSpider(scrapy.Spider):
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
            title = response.xpath("//ul[@class='parent']//li["+str(i)+"]/a/text()").extract()
            title = clsCore.unicodeTrans(title)
            if title == "Góc nhìn" or title == "Tất cả" or title == "Video": continue
            href = response.xpath("//ul[@class='parent']//li["+str(i)+"]/a/@href").extract()
            href = clsCore.unicodeTrans(href)
            z = clsCategories.insertOne(({"title":title}, {"url":href}))
            print(z)

    name = "crawlChildCate"
    def parse(self, response):
        clsCategories = Category()

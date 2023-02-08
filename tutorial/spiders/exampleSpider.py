import scrapy
from scrapy import signals

from scrapy.xlib.pydispatch import dispatcher
from tutorial.modelCustom.category.category import Category as Category
from tutorial.modelCustom.aa_core.core import Core as Core

class CrawlerSpider(scrapy.Spider):
    def __init__(self, type=None):
        self.count_request = 0
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        dispatcher.connect(self.spider_opened, signals.spider_opened)

    handle_httpstatus_list = [200, 403, 404, 400]
    name = "crawl_child_cate"
    allowed_domains = ["vnexpress.net"]

    def start_requests(self):
        clsCategories = Category()
        listCate = clsCategories.getAll(" order by id asc")

        if listCate is not None:
            for cate in listCate:
                self.count_request += 1
                metas = {
                    "id" : cate["id"],
                }
                yield scrapy.Request(url="https://vnexpress.net"+cate["url"], meta=metas)

    def parse(self, response):
        clsCore = Core()
        print("====================================================")
        for elmt in response.xpath("//ul[@class='ul-nav-folder']/li//a"):
            title = elmt.xpath("./text()").extract()
            href = elmt.xpath("./@href").extract()
            print ("title: "+clsCore.unicodeTrans(title[0]) + " | " + "href: "+clsCore.unicodeTrans(href[0]))
        

    def spider_closed(self):
        pass

    def spider_opened(self):
        pass  
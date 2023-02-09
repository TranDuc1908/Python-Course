import scrapy
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from ..items import ChildCategoryItem

from tutorial.modelCustom.category.category import Category as Category
from tutorial.modelCustom.aa_core.core import Core as Core

class CrawlerSpider(scrapy.Spider):
    handle_httpstatus_list = [200, 403, 404, 400]
    name = "crawl_child_cate"
    custom_settings = {
        # 'DOWNLOAD_DELAY': 2,
        'ITEM_PIPELINES': {
            'tutorial.pipelines.insertChildCatePipeline': 300,
        }
    }
    allowed_domains = ["vnexpress.net"]

    def __init__(self, type=None):
        self.count_request = 0
        self.itemCollection = []
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        dispatcher.connect(self.spider_opened, signals.spider_opened)

    def start_requests(self):
        clsCategories = Category()
        listCate = clsCategories.getAll(" order by id asc")

        if listCate is not None:
            for cate in listCate:
                compare = str(cate["url"]).strip()
                compare = compare[:4]
                if compare == "http": continue
                self.count_request += 1
                basicData = {"id" : cate["id"]}
                yield scrapy.Request(url="https://vnexpress.net"+cate["url"], callback= self.sendItemCollection, meta=basicData)
    
    def parse(self, response):
        clsCore = Core()
        if(response.xpath("//ul[@class='ul-nav-folder']/li//a")):
            for elmt in response.xpath("//ul[@class='ul-nav-folder']/li//a"):
                newItem = ChildCategoryItem()
                title = elmt.xpath("./text()").extract()
                title = clsCore.unicodeTrans(title[0])
                newItem["title"] = title
                url = elmt.xpath("./@href").extract()
                url = clsCore.unicodeTrans(url[0])
                newItem["url"] = url
                newItem["parent_id"] = response.meta.get("id")
                yield newItem

    def sendItemCollection(self, response):
        clsCore = Core()
        if(response.xpath("//ul[@class='ul-nav-folder']/li//a")):
            for elmt in response.xpath("//ul[@class='ul-nav-folder']/li//a"):
                newItem = ChildCategoryItem()
                title = elmt.xpath("./text()").extract()
                title = clsCore.unicodeTrans(title[0])
                newItem["title"] = title
                url = elmt.xpath("./@href").extract()
                url = clsCore.unicodeTrans(url[0])
                newItem["url"] = url
                newItem["parent_id"] = response.meta.get("id")
                self.itemCollection.append(newItem)

    def testFunction(self):
        print("=================================================================")
        print("Function go through here!")
        print("=================================================================")
        return True

    def spider_opened(self):
        pass  

    def spider_closed(self):
        print("=================================================================")
        print("Spider close arrived!")
        print("=================================================================")
        newItemCollection = self.itemCollection + self.itemCollection
        count = 1
        collectionToInsert = []
        clsCategories = Category()
        for item in newItemCollection:
            if count == 1000:
                for tmp in collectionToInsert:
                    record = [
                        {"title":tmp["title"]},
                        {"url":tmp["url"]},
                        {"parent_id":tmp["parent_id"]},
                    ]
                    res = clsCategories.insertOne(tuple(record))
                    if res == False:
                        print("================>Fail")
                        break
                collectionToInsert = []
                collectionToInsert.append(item)
                count = 2
            else:
                collectionToInsert.append(item)
                count +=1
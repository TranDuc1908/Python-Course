import scrapy
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from ..items import ChildCategoryItem
import datetime

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
    
    def arraySplitToChunk(self, xs, n):
        n = max(1, n)
        return (xs[i:i+n] for i in range(0, len(xs), n))

    def spider_opened(self):
        pass  

    def spider_closed(self):
        newItemCollection = self.itemCollection + self.itemCollection
        count = 0
        self.lastCollection = []
        self.bigCollection = []
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for item in newItemCollection:
            count+=1
            self.bigCollection.append((item["title"],item["url"],item["parent_id"], time))
        self.lastCollection = self.arraySplitToChunk(self.bigCollection, 1000)
        clsCategories = Category()
        print("=====================> start loop")
        for z in self.lastCollection:
            sqlQry = "INSERT INTO categories (`title`, `url`, `parent_id`, `created_at`) VALUES (%s, %s, %s, %s)"
            c = clsCategories.testInsertAll(sqlQry,z)
            print("=============================> RESULT")
            print(c)


            # for item in z:
            #     print(type(item))
            #     print(item)
            #     break
            #     for key in item:
            #         if int(key)%1000 == 0:
            #             print(item)
            # break
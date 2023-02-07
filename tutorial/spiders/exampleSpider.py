import scrapy
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class CrawlerSpider(scrapy.Spider):
    def __init__(self, type=None):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        dispatcher.connect(self.spider_opened, signals.spider_opened)

    handle_httpstatus_list = [200, 403, 404, 400]
    name = "name_spider"
    allowed_domains = ["example.com"]

    def start_requests(self):
        yield scrapy.Request("https://example.com")

    def parse(self, response): 
        pass

    def spider_closed(self, spider, reason):
        pass

    def spider_opened(self, spider, reason):
        pass  
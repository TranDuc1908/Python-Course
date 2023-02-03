import scrapy
from tutorial.modelCustom.category.category import Category as Category

class QuotesSpider(scrapy.Spider):
    name = "crawlCate"
    startUrl = "https://vnexpress.net/"
    clsCategories = Category()
    clsCategories.showInfo()


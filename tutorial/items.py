# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CategoryItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    
class ChildCategoryItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    parent_id = scrapy.Field()
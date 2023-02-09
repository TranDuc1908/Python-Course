# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from tutorial.modelCustom.category.category import Category as Category
from tutorial.modelCustom.aa_core.core import Core as Core


class TutorialPipeline(object):
    def process_item(self, item, spider):
        print("================ Custom pipeline arrived ================")
        print(item["parent_id"])
class insertChildCatePipeline(object):
    def process_item(self, item, spider):
        print("================ Pipeline arrived ================")
        clsCategories = Category()
        data = [
            {"parent_id": item["parent_id"]},
            {"title": item["title"]},
            {"url": item["url"]},
        ]
        
        res = clsCategories.insertOne(tuple(data))
        try: res
        except NameError: res = None
        if res is None:
            print("Insert to DB fail!")
        else:
            print("Insert to DB success!")


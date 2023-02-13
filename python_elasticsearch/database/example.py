# -*- coding: utf-8 -*-
from elasticsearch2 import Elasticsearch
import datetime

es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}])
# print(es.ping())

index = "category"

def insertOne(_index, data):
    res = es.index(index=_index, doc_type="parentCate", id=None, body=data)
    print("=========> Create result:")
    print(res)

def getOne(_index, _id):
    res = es.get(index=_index, id=_id)
    print("=========> Read by id result:")
    print(res)

def updateOne(_index, _id, _body):
    res = es.index(index=_index, doc_type="parentCate", id=_id, body=_body)
    print("=========> Update result:")
    print(res)


dataToCreate = {
    "title": "Thời sự",
    "url": "/thoi-su",
    "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

dataToUpdate = {
    'doc': {
        "title": "Thời sự Updated-version",
        "url": "/thoi-su",
        "updated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
}


# insertOne(index, dataToCreate)
getOne(index, "AYZKQ_5M15KoxUaf1285")
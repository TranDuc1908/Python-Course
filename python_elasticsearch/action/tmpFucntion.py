# -*- coding: utf-8 -*-
import datetime
import requests
import json

mapping = '''
            {
                "mappings" : {
                    "category" : {
                        "properties" : {
                            "title" : { "type" : "string"},
                            "slug" : { "type" : "string"},
                            "url" : { "type" : "string"},
                            "parent_id" : { "type" : "string"},
                            "created_at":{"type":"date","format":"dd/MM/yyyy HH:mm:ss"},
                            "updated_at":{"type":"date","format":"dd/MM/yyyy HH:mm:ss"},
                            "deleted_at":{"type":"date","format":"dd/MM/yyyy HH:mm:ss"}
                        }
                    }
                }
            }
        '''

_url = "http://localhost:9200/categories"
try:
    resp = requests.put(url=_url, data=mapping, headers={'Content-Type': 'application/json'}) 
    print(resp.json())
except:
    print("=============== Create index fail ===============")
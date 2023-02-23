import requests


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
                    },
                    "news" : {
                        "properties" : {
                            "title" : { "type" : "string"},
                            "intro" : { "type" : "string"},
                            "slug" : { "type" : "string"},
                            "url" : { "type" : "string"},
                            "category_id" : { "type" : "string"},
                            "author" : { "type" : "string"},
                            "published_at":{"type":"date","format":"dd/MM/yyyy HH:mm:ss"},
                            "created_at":{"type":"date","format":"dd/MM/yyyy HH:mm:ss"},
                            "updated_at":{"type":"date","format":"dd/MM/yyyy HH:mm:ss"},
                            "deleted_at":{"type":"date","format":"dd/MM/yyyy HH:mm:ss"}
                        }
                    }
                }
            }
        '''

domain = 'http://localhost:9200/'
_url = domain + "project"

try:
    resp = requests.put(url=_url, data=mapping, headers={'Content-Type': 'application/json'}) 
    print(resp.json())
except:
    print("=============== Create index fail ===============")

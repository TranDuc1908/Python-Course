import json
import requests

class CoreDatabase():
    def __init__(self):
        self.host = "http://localhost:9200"
        self.limit = 1000

    def getAllDocument(self, page, index, type=""):
        payload = json.dumps({
            "query": {"match_all": {}},
            "from": page*self.limit,
            "size": self.limit
        })

        url = self.host + "/" + index + "/" + type + "/_search"

        response = requests.request("GET", url, data=payload)
        resp = json.loads(response.text)
        # return len(resp["hits"]["hits"])
        if not resp["hits"]["hits"]: return {"res":False}
        else: return {"res":True, "data":resp["hits"]["hits"]} 


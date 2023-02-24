import json
import requests
import datetime 

class CoreDatabase():
    def __init__(self):
        self.host = "http://localhost:9200"
        self.limit = 1000
        self.headerConfig = {'Content-Type': 'application/json'}

    def getAllDocument(self, page, index="project", type=""):
        payload = json.dumps({
            "query": {"match_all": {}},
            "from": page*self.limit,
            "size": self.limit
        })

        url = self.host + "/" + index + "/" + type + "/_search"

        response = requests.request("GET", url, data=payload)
        resp = json.loads(response.text)
        # return len(resp["hits"]["hits"])
        if bool(resp["status"]) is not False and resp["status"] != 200: return {"res":False,"data":resp["error"]}
        else: return {"res":True, "data" : resp["hits"]["hits"]}

    def insertOne(self,_dict,_type):
        _data = dict()
        _data["doc"] = _dict
        _data["doc"]["created_at"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        _data = json.dumps(_dict)
        _url = self.host + "project/" + _type
        try:
            resp = requests.post(_url, data=_data, headers=self.headerConfig)
            resp = resp.json()
            return resp
        except:
            return False
        
    def updateProperties(self, _type, id, _dict):
        _data = dict()
        _data["doc"] = _dict
        _data["doc"]["updated_at"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        _data = json.dumps(_data)
        url = self.host + "project/"+_type+"/"+id+"/_update"
        resp = requests.post(url=url, data=_data, headers=self.headerConfig)
        return resp


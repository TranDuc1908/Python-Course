# encoding: utf-8
import json
import requests

url = "http://localhost:9200/project/news/_search"
i=0
payload = json.dumps({
"query": { "match_all": {} },
"from": i*1000,
"size": 1000
})
response = requests.request("GET", url, data=payload)
resp = json.loads(response.text)

for item in resp["hits"]["hits"]:
    url = "http://localhost:9200/project/news/"+item["_id"]
    response = requests.request("DELETE", url)
    print(response)
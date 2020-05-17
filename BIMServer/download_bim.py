import json
import requests
import time
import os

with open('bimserver.json', 'r') as f:
    output = json.load(f)

url = "http://data.ksd.ai.ar.tum.de:8080/json"
download_url = "http://data.ksd.ai.ar.tum.de:8080/download"
download_path = 'D:\OneDrive\TUM\SoSe 19\Algorithmic Design\Project\Dataset\BIMServer\IFC Files'

headers = {
    'Cookie': "_ga=GA1.2.2046203334.1562320460; autologin8080=8eb30312e5690c32f1a394e549b3524d19d3b2e5165c0fd9c7f802b8d89287388a88269e29312e0d85db7ce5158e76e4; address8080=http%3A%2F%2Fdata.ksd.ai.ar.tum.de%3A8080; JSESSIONID=EA5C44B5B1473DDBDB15C459144D6BB7",
    'Origin': "http://data.ksd.ai.ar.tum.de:8080",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "en-US,en;q=0.9",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
    'Content-Type': "application/json",
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Referer': "http://data.ksd.ai.ar.tum.de:8080/?page=Project&poid=18874369",
    'X-Requested-With': "XMLHttpRequest",
    'Connection': "keep-alive",
    'Cache-Control': "no-cache",
    'Postman-Token': "14d9bdac-65ff-4f99-a680-383eb745f1cf,55863558-9ad8-4c70-886a-07900c7a2c8a",
    'Host': "data.ksd.ai.ar.tum.de:8080",
    'content-length': "350",
    'cache-control': "no-cache"
}
download_headers = {
    'Connection': "keep-alive",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    'Referer': "http://data.ksd.ai.ar.tum.de:8080/?page=Project&poid=7602177",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "en-US,en;q=0.9",
    'Cookie': "_ga=GA1.2.2046203334.1562320460; autologin8080=8eb30312e5690c32f1a394e549b3524d19d3b2e5165c0fd9c7f802b8d89287388a88269e29312e0d85db7ce5158e76e4; address8080=http%3A%2F%2Fdata.ksd.ai.ar.tum.de%3A8080; JSESSIONID=EA5C44B5B1473DDBDB15C459144D6BB7",
    'Cache-Control': "no-cache",
    'Postman-Token': "7ae2d824-e93c-48bb-b3a6-6202998c7c74,3d8b53a8-758a-463b-85f2-29e6529fde8e",
    'Host': "data.ksd.ai.ar.tum.de:8080",
    'cache-control': "no-cache"
}

for index, result in enumerate(output['response']['result']):
    if index < 12:
        continue
    if result['lastRevisionId'] > 0:
        payload = {
            "request": {
                "interface": "org.buildingsmart.bimsie1.Bimsie1ServiceInterface",
                "method": "download",
                "parameters": {
                    "downloadType": "single",
                    "allowCheckouts": True,
                    "poid": result['oid'],
                    "roid": result['lastRevisionId'],
                    "serializerOid": "917542",
                    "showOwn": True,
                    "sync": False
                }
            },
            "token": "8eb30312e5690c32f1a394e549b3524d19d3b2e5165c0fd9c7f802b8d89287388a88269e29312e0d85db7ce5158e76e4"
        }

        response = requests.request("GET", url, json=payload, headers=headers)
        response = response.json()


        querystring = {
            "token": "8eb30312e5690c32f1a394e549b3524d19d3b2e5165c0fd9c7f802b8d89287388a88269e29312e0d85db7ce5158e76e4",
            "longActionId": str(response['response']['result']),
            "serializerOid": "917542"
        }

        file_name = result['name'].replace("?", "")
        print("Downloading %s , %d" % (file_name, response['response']['result']))

        download_response = requests.request("GET", download_url, headers=download_headers, params=querystring)
        with open(os.path.join(download_path, file_name), 'wb') as f:
            f.write(download_response.content)

        time.sleep(5)
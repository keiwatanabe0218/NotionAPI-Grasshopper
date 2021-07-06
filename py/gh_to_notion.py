# coding: -*- utf-8 -*-
import scriptcontext as sc
import Rhino

sc.doc = Rhino.RhinoDoc.ActiveDoc

# APIリクエスト用のimport
from System.Net import WebRequest
from System.Text import ASCIIEncoding
from System.IO import StreamReader
from System.Net import ServicePointManager
from System.Net import SecurityProtocolType
from System.Net import WebException
import time, json

# APIリクエストを送る関数
def http(method, url, data_string=None, header={}, retry=3):
    ServicePointManager.SecurityProtocol |= SecurityProtocolType.Tls11 | SecurityProtocolType.Tls12
    request = WebRequest.Create(url)
    request.UseDefaultCredentials = True
    request.Method = method
    request.ContentLength = 0
    
    for k,v in header.items():
        request.Headers.Add(k,v)
    
    if data_string:
        request.ContentType = "application/json"
        encoding = ASCIIEncoding()
        data = encoding.GetBytes(data_string)
        request.ContentLength = data.Length
        stream = request.GetRequestStream()
        stream.Write(data, 0, data.Length)
        stream.Close()

    try:
        response = request.GetResponse()
        print (response.StatusDescription)
        dataStream = response.GetResponseStream()
        reader = StreamReader(dataStream)
    
        responseFromServer = reader.ReadToEnd()
            
        reader.Close()
        dataStream.Close()
        response.Close()
        return responseFromServer

    except WebException as e : 
        if e.Response.StatusDescription == "Not Found" and retry>0:
            time.sleep(10)
            return http(method, url, data_string, header, retry-1)

        print (e.Response.StatusDescription)
        dataStream = e.Response.GetResponseStream()
        reader = StreamReader(dataStream)
    
        responseFromServer = reader.ReadToEnd()
        print (responseFromServer)
    
        reader.Close()
        dataStream.Close()



if __name__ == "__main__":
    # オブジェクト情報を整理
    objects = []
    for geo in geometries:
        attr = {}
        obj = sc.doc.Objects.Find(geo)
        attr["GUID"] = str(obj.Attributes.ObjectId)
        attr["Layer"] = sc.doc.Layers.FindIndex(obj.Attributes.LayerIndex).FullPath
        attr["Type"] = str(obj.GetType())
        objects.append(attr)
        print(attr)
    # HTTPリクエストを作成
    # URL
    url = "https://api.notion.com/v1/pages"
    # Token
    token = "Bearer {{TOKEN}}"
    # headers
    headers = {
                'Authorization': token,
                'Notion-Version': "2021-05-13",
                }
    # オブジェクトごとにbodyを作ってPOST
    if run:
        for obj in objects:
            values = {
                "parent": {"database_id": "{{DATABASE_ID}}"},
                "properties": {
                    "GUID": {
                        "title": [
                            {
                            "text": {
                                "content": obj["GUID"]
                                }
                            }
                        ]
                    },
                    "Layer": {
                        "select": 
                            {
                            "name":obj["Layer"]
                            }
                    },
                    "Type": {
                        "select": 
                            {
                            "name":obj["Type"]
                            }
                    },
                }
                }
            # bodyを文字列化
            data = json.dumps(values)
            # POST
            http("POST",url,data,headers)
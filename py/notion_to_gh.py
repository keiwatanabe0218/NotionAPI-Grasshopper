from System.Net import WebRequest
from System.Text import ASCIIEncoding
from System.IO import StreamReader
from System.Net import ServicePointManager
from System.Net import SecurityProtocolType
from System.Net import WebException
import time, json

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
    database_id = "{{DATABASE_ID}}"
    # URL
    url = "https://api.notion.com/v1/databases/{}/query/".format(database_id)
    # Token
    token = "Bearer {{TOKEN}}"
    # headers
    headers = {
                'Authorization': token,
                'Notion-Version': "2021-05-13",
                }
    # body
    values = {
                "filter":{
                    "property": "Create",
                    "checkbox": {
                        "equals": True
                    }
                }
    }
    data = json.dumps(values)
    
    # リストを初期化
    X = []
    Y = []
    Z = []
    W = []
    D = []
    H = []
    Color = []
    # POST
    if run:
        res = http("POST",url,data,headers)
    		# dictionaryに変換して"results"を取り出す
        objects = json.loads(res)["results"]
        for obj in objects:
    				# properties情報を取り出す
            props = obj["properties"]
    				# 各変数を取り出してリストに追加
            create = props["Create"]["checkbox"]
            X.append(props["X"]["number"])
            Y.append(props["Y"]["number"])
            Z.append(props["Z"]["number"])
            W.append(props["W"]["number"])
            D.append(props["D"]["number"])
            H.append(props["H"]["number"])
            Color.append(props["Color"]["select"]["name"])
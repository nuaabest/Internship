import hmac
import base64
import datetime
import time
import urllib.parse
import urllib.request
import requests
import sys
import os
import json
import pandas as pd
#TODO 数据不使用科学计数法

def unicode2utf8(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, str):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ unicode2utf8(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            unicode2utf8(key, ignore_dicts=True): unicode2utf8(value, ignore_dicts=True)
            for key, value in data.items()
            }
    # if it's anything else, return it in its original form
    return data

class mail:
    apiKey = 
    apiSecret=
    accountName ='info@m.beavotech.com'
    def sign(self,message):
        h = hmac.new(str.encode(self.apiSecret), str.encode(message), digestmod = 'sha1')
        return base64.b64encode(h.digest())
    def constructParam(self, title, content, targets):
        timestamp = datetime.datetime.utcnow().isoformat()
        print(time.time())
        nonce = str(time.time())+'.ss'
        dicParams = {}
        dicParams["AccessKeyId"] = self.apiKey
        dicParams["AccountName"] = self.accountName
        dicParams["Action"] = "SingleSendMail"
        dicParams["AddressType"]="1"
        dicParams["Format"] = "JSON"
        dicParams["HtmlBody"] = content
        dicParams["RegionId"] = "cn-hangzhou"
        dicParams["ReplyToAddress"] = "false"
        dicParams["SignatureMethod"] = "HMAC-SHA1"
        dicParams["SignatureNonce"] = nonce
        dicParams["SignatureVersion"] = "1.0"
        dicParams["Subject"] = title
        dicParams["Timestamp"] = timestamp
        dicParams["ToAddress"] = targets
        dicParams["Version"] = "2015-11-23"
        return unicode2utf8(dicParams)
    def constructMessage(self,dicParams):
        method = 'GET'
        queryParam = urllib.parse.urlencode(dicParams)
        queryParam = queryParam.replace('+','%20')
        dataToSign = method + '&%2F&' + urllib.parse.quote(queryParam)
        return dataToSign
    def sendMail(self, title, content, targets):
        dictParams = self.constructParam(title, content, targets)
        dataToSign = self.constructMessage(dictParams)
        signedData = self.sign(dataToSign)
        print(dictParams)
        print(dataToSign)
        print(signedData)
        dictParams['Signature'] = signedData
        r = requests.get('http://dm.aliyuncs.com/', params = dictParams)
        print(r.text)

def convertToHtml(result_1, title_1, result_2, title_2, datatype):
    #将数据转换为html的table
    #result是list[list1,list2]这样的结构
    #title是list结构；和result一一对应。titleList[0]对应resultList[0]这样的一条数据对应html表格中的一列
    head = \
        """
        <head>
            <meta charset="utf-8">
            <STYLE TYPE="text/css" MEDIA=screen>

                table.dataframe {
                    border-collapse: collapse;
                    border: 2px solid #a19da2;
                    /*居中显示整个表格*/
                    margin: auto;
                }

                table.dataframe thead {
                    border: 2px solid #91c6e1;
                    background: #f1f1f1;
                    padding: 10px 10px 10px 10px;
                    color: #333333;
                }

                table.dataframe tbody {
                    border: 2px solid #91c6e1;
                    padding: 10px 10px 10px 10px;
                }

                table.dataframe tr {

                }

                table.dataframe th {
                    vertical-align: top;
                    font-size: 14px;
                    padding: 10px 10px 10px 10px;
                    color: #105de3;
                    font-family: arial;
                    text-align: center;
                }

                table.dataframe td {
                    text-align: center;
                    padding: 10px 10px 10px 10px;
                }

                body {
                    font-family: 宋体;
                }

                h1 {
                    color: #5db446
                }

                div.header h2 {
                    color: #0002e3;
                    font-family: 黑体;
                }

                div.content h2 {
                    text-align: center;
                    font-size: 28px;
                    text-shadow: 2px 2px 1px #de4040;
                    color: #fff;
                    font-weight: bold;
                    background-color: #008eb7;
                    line-height: 1.5;
                    margin: 20px 0;
                    box-shadow: 10px 10px 5px #888888;
                    border-radius: 5px;
                }

                h3 {
                    font-size: 22px;
                    background-color: rgba(0, 2, 227, 0.71);
                    text-shadow: 2px 2px 1px #de4040;
                    color: rgba(239, 241, 234, 0.99);
                    line-height: 1.5;
                }

                h4 {
                    color: #e10092;
                    font-family: 楷体;
                    font-size: 20px;
                    text-align: center;
                }

                td img {
                    /*width: 60px;*/
                    max-width: 300px;
                    max-height: 300px;
                }

            </STYLE>
        </head>
        """
    body = \
        """
        <body>
        <h1>{}</h1>
        <div align="center" class="header">
            <!--标题部分的信息-->
        </div>

        <hr>

        <div class="content">
            <!--正文内容-->
            <h2> </h2>

            <div>
                <h4></h4>
                {}
            </div>
            <hr>

            <p style="text-align: center">

            </p>
        </div>

        <div align="center" class="header">
            <!--标题部分的信息-->
        </div>

        <hr>

        <div class="content">
            <!--正文内容-->
            <h2> </h2>

            <div>
                <h4></h4>
                {}
            </div>
            <hr>

            <p style="text-align: center">

            </p>
        </div>
        </body>
        """
    d1 = {}
    d2 = {}
    index = 0
    for t in title_1:
        d1[t] = result_1[index]
        index = index + 1
    
    df = pd.DataFrame(d1)

    index = 0
    for t in title_2:
        d2[t] = result_2[index]
        index = index + 1

    df1 = pd.DataFrame(d2)
    
    h = df.to_html(index = False, justify = 'center', col_space = 100)
    h2 = df1.to_html(index = False, justify = 'center', col_space = 100)
    if datatype == '105':
        return '<html>'+ head + body.format(datatype, h, h2) + '</html>'
    else:
        return '<html>'+ head + body.format(datatype, h, h2) + '</html>'

if __name__=='__main__':
    if len(sys.argv) != 3:
        print('command like: python3 {} 2020-05-01 [datatype] [server_name]'.format(sys.argv[0]))
        sys.exit(-1)
    date = sys.argv[1]
    dataType = sys.argv[2]
    truePath = date + dataType
    currntPath = os.path.join(os.getcwd(), truePath)
    
    exchange = []
    exActualCount = []
    exTheoCount = []

    dataMedian = []
    dataStd = []
    coinpairs = []

    breakTime = []
    server_name = ""
    docker_name = ""
    if sys.argv[3] == "IRL-Deribit":
        sn = sys.argv[3].split('-')[0]
    else:
        sn = sys.argv[3]
    with open("/liandao/lcy-scripts/config" + sn + ".json") as config_file:
        config = json.load(config_file)
        server_name = config["server_name"] if "server_name" in config else "default server"
        docker_name = config["docker_name"] if "docker_name" in config else "default docker"

    os.chdir(currntPath)
    #currentPath现在就是对应类型的数据一天的json文件存放路径
    for files in os.listdir(os.getcwd()):
        if '.json' not in files:
            continue
            
        with open(files, 'r') as f:
            jsonData = json.load(f)
            for name, data in jsonData.items():
                exchange.append(name)
                exActualCount.append(data['actual_pairs_count'])
                exTheoCount.append(data['theo_pairs_count'])
                coinpair = data['pairs']
                if dataType == '105':
                    for coin in coinpair:
                        coinpairs.append(coin)
                        dataStd.append(data[coin]['std'])
                        dataMedian.append(data[coin]['median'])
                else:
                    for coin in coinpair:
                        if data[coin]['breaktimes'] != 0:
                            coinpairs.append(coin)
                            breakTime.append(data[coin]['breaktimes'])


    if len(exchange) == 0 or len(exActualCount) == 0 or len(exTheoCount) == 0 or len(coinpairs) == 0:
        print("no data valid")
        sys.exit()
    titles_1 = ['exchange', 'pairs count', 'actual pairs count']
    contents_1 = [exchange, exTheoCount, exActualCount]
    if dataType == '105':
        titles_2 = ['coinpairs', 'coin_std', 'coin_median']
        contents_2 = [coinpairs, dataMedian, dataStd]
    elif dataType == '106':
        titles_2 = ['coinpairs', 'break_times']
        contents_2 = [coinpairs, breakTime]

    table = convertToHtml(contents_1, titles_1, contents_2, titles_2, dataType)
    table = table.replace('\n','')
    table = table.replace('\t','')
    table = table.replace('\r','')
    
    mailInstance = mail()
    mailInstance.sendMail('{}@{} {}'.format(docker_name, server_name, date), table, '1728951866@qq.com')

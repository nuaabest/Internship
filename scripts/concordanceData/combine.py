# *=======================================================*
# -*- coding:utf-8 -*-
# * time : 2020-03-24 19:34
# * author : lichengyi
# *=======================================================*
# combine data
'''
在concordance_data.py以及将数据按照n个压缩包分好币对，这个脚本
负责将那些币对信息合并起来
'''
import os
import sys
import pandas as pd
import codecs
import time

nowtime = time.strftime('%Y', time.localtime(time.time()))
path = "/liandao/yjj_data/" + sys.argv[1]
server = sys.argv[2]
coinInfo = {}
exTK15 = ["binance", "binancef", "hbdm", "huobi"]
ttime = ["2020-03-02", "2020-03-03", "2020-03-04", "2020-03-05", "2020-03-06", "2020-03-07"]

def combine():
    os.chdir(path)
    dirs = os.listdir(path)
    for file in dirs:
        if os.path.isdir(file) != True:
            continue
        else:
            os.chdir("./" + file)
            cdirs = os.listdir(os.getcwd())
            for cfile in cdirs:
                if os.path.isdir(cfile) != True:
                    continue
                else:
                    os.chdir("./" + cfile)
                    fdirs = os.listdir(os.getcwd())
                    print("now is in " + os.getcwd())
                    for ffile in fdirs:
                        if os.path.isfile(ffile) != True:
                            continue
                        if nowtime not in ffile:
                            continue
                        else:
                            coin = ffile.split('_', 1)[1].split('.', 1)[0]
                            if coin not in coinInfo:
                                coinInfo[coin] = []
                                coinInfo[coin].append(ffile)
                                coinInfo[coin].sort(reverse = False)
                            else:
                                coinInfo[coin].append(ffile)
                                coinInfo[coin].sort(reverse = False)
                    coinFinCom(coinInfo, server)
                    os.chdir("../")
                    coinInfo.clear()
            os.chdir("../")

    return

def coinFinCom(coin, server):
    for k in coin:
        result = k + ".csv"
        re = codecs.open(result, 'ab+', encoding = "utf-8")
        print(k + ":" + coin[k][0])
        fi = open(coin[k][0], 'r')
        contents = fi.readlines()
        re.writelines(contents)
        fi.close()
        cmd = "rm -rf ./" + coin[k][0]
        os.system(cmd)
        for i in range(1, len(coin[k])):
            print(k + ":" + coin[k][i])
            #此时的文件名是coin[k][i]
            lines = open(coin[k][i], 'r').readlines()
            re.writelines(lines[1:])
            cmd = "rm -rf ./" + coin[k][i]
            os.system(cmd)
        
        if server != "TK10":
            nowPath = os.getcwd()
            Path = nowPath.split('/')
            cmd1 = "zip " + Path[5] + "-" + Path[6] + "-" + Path[7] + "-" + k + ".zip " + result
            cmd2 = "mv " + Path[5] + "-" + Path[6] + "-" + Path[7] + "-" + k + ".zip " + "/liandao/data-backup"
            os.system(cmd1)
            if server == "TK15" and Path[6] in exTK15:
                os.system(cmd2)
            if server == "TK15" and Path[6] == "bequant":
                if Path[5] == "2020-03-02" or Path[5] == "2020-03-03" or Path[5] == "2020-03-05":
                    os.system(cmd2)
            if server == "TK15" and Path[6] == "bitmex":
                if Path[5] in ttime:
                    os.system(cmd2)
            if server == "TK15" and Path[6] == "deribit":
                if Path[5] in ttime:
                    os.system(cmd2)

            if server == "IRL-Deribit":
                os.system(cmd2)
        re.close()
        
    return

combine()

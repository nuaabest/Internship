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

path = "/liandao/yjj_data/" + sys.argv[1]
coinInfo = {}

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
                        else:
                            coin = ffile.split('_', 1)[1].split('.', 1)[0]
                            if coin not in coinInfo:
                                coinInfo[coin] = []
                                coinInfo[coin].append(ffile)
                                coinInfo[coin].sort(reverse = False)
                            else:
                                coinInfo[coin].append(ffile)
                                coinInfo[coin].sort(reverse = False)
                    coinFinCom(coinInfo)
                    os.chdir("../")
                    coinInfo.clear()
            os.chdir("../")

    return

def coinFinCom(coin):
    for k in coin:
        result = k + ".csv"
        re = codecs.open(result, 'ab+', encoding = "utf-8")
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

        re.close()

    return

combine()

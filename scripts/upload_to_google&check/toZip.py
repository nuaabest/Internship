# *=======================================================*
# -*- coding:utf-8 -*-
# *   time : 2020-04-22 9:00
# * author : lichengyi
# *=======================================================*
'''
针对3月25号到4月19号之间的已经存放在北京的/liandao/yjj_md_data/
文件夹下的东京15和IRL-Deribit的压缩包，将其解压并将所有的币对csv
单独压缩传到新加坡
'''
import os
import multiprocessing

path = "/liandao/yjj_md_data/"

def toZip(server):
    count = 0
    truePath = path + server
    os.chdir(truePath)
    dirs = os.listdir(truePath)
    for file in dirs:
        count += 1
        cmd = "unzip -o -d " + truePath + "file_" + str(count)\
            + " " + file
        date = file.split('-', 1)[1].split('.', 1)[0]
        os.system(cmd)
        p = multiprocessing.Process(target = coinToZip, args = \
            (truePath, date, server, count))
        p.start()
    return 

def coinToZip(filePath, date, server, count):
    nowPath = filePath + "file_" + str(count) + "/liandao/yjj_data/" + server + "md/" + date
    dirs1 = os.listdir(nowPath)
    for dir1 in dirs1:
    #进入交易所的文件夹
        os.chdir("./" + dir1)
        dirs2 = os.listdir(os.getcwd())
        for dir2 in dirs2:
        #进入类型的文件夹
            os.chdir("./" + dir2)
            files = os.listdir(os.getcwd())
            for file in files:
                coinName = file.split('_', 1)[1].split('.', 1)[0]
                zipFile = date + "-" + dir1 + "-" + dir2 + "-"\
                    + coinName + ".zip"
                cmd = "zip " + filePath + "/" + zipFile + " "\
                    + file
                os.system(cmd)
            os.chdir("../")
        os.chdir("../")

    cmd = "rm -rf " + filePath + "file_" + str(count)
    os.system(cmd)
    return

toZip("TK15/")
toZip("IRL-Deribit/")
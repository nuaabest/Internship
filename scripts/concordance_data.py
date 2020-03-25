# *=======================================================*
# -*- coding:utf-8 -*-
# * time : 2020-03-18 15:34
# * author : lichengyi
# *=======================================================*
# concordance data
'''
1、首先把一个日期文件内的所有压缩文件全部解压缩存放格式为shared1
2、扫描所有解压缩的文件，发现一个交易所的名称就产生一个对应的文件夹，
   同时把此时的文件存放进去对应的文件夹，按照在cp进去的文件中加上时
   间，如果已存在就不用
3、然后再对每个交易所进行操作，扫描每个交易所里面的文件夹，按照后缀
   进行分类并产生新的文件夹
采用多进程的方式将48个时间点的压缩包同时进行处理，然后再合并即可
运行方式：sudo python3 concordance_data.py [交易所]/[docker]/[日期]
实际上的路径应该具体条件具体给出，但是北京存放的路径是上面形式

unzupFile、diffExchange、diffType只是用来对文件进行分类
'''
import os
import sys
import multiprocessing
import pandas as pd
import csv

path = "/liandao/yjj_data/" + sys.argv[1]
mid_path = "/shared/performance_report/data"

exchange = []
coinInfo = []
typeInfo = []
saveData = ""

#这个函数只是用来进行解压缩
def unzipFile():
   print("unzip start")
   os.chdir(path)
   dirs = os.listdir(path)
   count = 0   
   for file in dirs:
      if os.path.isfile(file) != True:
         continue
      else:
         count += 1
         cmd = "unzip -o -d " + path + "/shared_" + str(count) + " " + file
         os.system(cmd)
         #在产生一个文件夹之后就可以对这个文件夹进行扫描
         #以产生对应的交易所目录
         finName = file.split('_', 1)[0]
         p = multiprocessing.Process(target = diffExchange, args=(path, finName, count))
         p.start()
         
      os.chdir(path)
   print("unzip end")
   return

#这个函数将解压缩的文件夹里面的csv文件分交易所存放并按次序取名
def diffExchange(file, finName, count):
   print("exchange start")
   filePath = file + "/shared_" + str(count) + mid_path
   os.chdir(filePath)
   dirs = os.listdir(filePath)
   for cfile in dirs:
      if os.path.isfile(cfile) != True:
         continue
      else:
         exchangeName = cfile.split('_', 1)[0]
         fullName = cfile.split('.', 1)[0]
         if exchangeName not in exchange:
            exchange.append(exchangeName)
            os.chdir(path)
            if os.path.exists(path + exchangeName) != True:
               cmd = "mkdir " + exchangeName
               os.system(cmd)
               
         os.chdir(filePath)
         newName =  finName + "_" + fullName + "_" + ".csv"
         cmd = "mv " + filePath + "/" + cfile + " " + newName
         os.system(cmd)

         cmd = "mv " + filePath + "/" + newName + " " + path + "/" + exchangeName
         os.system(cmd)
         

   os.chdir(path)
   diffType(finName, count)
   print("exchang end")
   return

#这个函数就是将同一个交易所的105、106这种分类型存放
def diffType(finName, count):
   print("type start")
   dirs = os.listdir(path)
   for file in dirs:
      if file not in exchange:
         continue
      else:
         os.chdir(path + "/" + file)
         mdirs = os.listdir(os.getcwd())
         for mfile in mdirs:
            if os.path.isfile(path + "/" + file + "/" + mfile) != True:
               continue
            else:
               dataType = mfile.split('_', 3)[2]
               if dataType not in typeInfo:
                  typeInfo.append(dataType)

               if os.path.exists(path + "/" + file + "/" + dataType) != True:
                  if dataType == "106":
                     dataType = "book"
                  elif dataType == "105":
                     dataType = "trade"
                  elif dataType == "110":
                     dataType = "kline"
                  if dataType != "204" and dataType != "205" and dataType != "206" and dataType != "207":     
                     cmd = "mkdir " + path + "/" + file + "/" + dataType
                     os.system(cmd)
               
               if dataType != "204" and dataType != "205" and dataType != "206" and dataType != "207":
                  cmd = "mv " + path + "/" + file + "/" + mfile + " " + path + "/" + file + "/" + dataType
                  os.system(cmd)
               
                  os.chdir(path + "/" + file + "/" + dataType)
                  diffCoin(os.getcwd(), path + "/" + file + "/" + dataType + "/" + mfile, finName, mfile)
                  cmd = "rm -rf " + path + "/" + file + "/" + dataType + "/" + mfile
                  os.system(cmd)

               cmd = "rm -rf " + path + "/" + file + "/" + mfile
               os.system(cmd)

   typeInfo.clear()
   cmd = "rm -rf " + path + "/shared_" + str(count)

   os.system(cmd)
   print("type end")
   return

#下面这个函数是真正开始将相同币对集中起来
def diffCoin(truePath, filename, finName, mfile):
   print("coin start")
   newFile = ""
   nowType = truePath.rsplit('/',1)[1]
   flagtype = 0
   
   dirs = os.listdir(truePath)
   if os.path.exists(filename) != True:
      print("don't exist this file:" + filename)
      return
   flag = 0   
   for file in dirs:
      if file != mfile:
         continue
      elif os.path.getsize(filename) == 0:
         print("this file " + filename + " is empty")
      else:
         outFile = open(filename, 'r')
         csv_file = csv.reader(outFile)
         for row_data in csv_file:
            if flag == 0:
               saveData = row_data
               flag += 1
               continue
            else:
               if nowType == "trade":
                  newFile = finName + "_" + row_data[2] + ".csv"
               elif nowType == "book":
                  newFile = finName + "_" + row_data[0] + ".csv"
               elif nowType == "kline":
                  newFile = finName + "_" + row_data[1] + ".csv"
               
               if os.path.exists(newFile) != True:                                 
                  cmd = "touch " + truePath + "/" + newFile
                  os.system(cmd)
                  flagtype = 1
               
               inFile = open(newFile, 'a', newline='')
 
               csv_write = csv.writer(inFile, dialect='excel')
               if flagtype == 1:
                  csv_write.writerow(saveData)
                  flagtype = 0
               
               csv_write.writerow(row_data)               
            flag += 1 
      
   print("coin end")
   return


unzipFile()
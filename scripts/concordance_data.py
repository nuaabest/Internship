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
运行方式：sudo python3 concordance_data.py [交易所]/[docker]/[日期]
实际上的路径应该具体条件具体给出，但是北京存放的路径是上面形式

unzupFile、diffExchange、diffType只是用来对文件进行分类
'''
import os
import sys
#import pandas as pd
import csv

path = "/liandao/yjj_data/" + sys.argv[1]
mid_path = "/shared/performance_report/data"

exchange = []
coinInfo = []
typeInfo = []
saveData = ""

#这个函数只是用来进行解压缩
def unzipFile():
   os.chdir(path)
   count = 0
   dirs = os.listdir(path)
   for file in dirs:
      if os.path.isfile(file) != True:
         continue
      else:
         cmd = "unzip -o -d . " + file
         os.system(cmd)
         #在产生一个文件夹之后就可以对这个文件夹进行扫描
         #以产生对应的交易所目录
         diffExchange(path, count)
         count += 1
         os.chdir(path)
         cmd = "rm -rf ./shared"
         os.system(cmd)
      os.chdir(path)
   return

#这个函数将解压缩的文件夹里面的csv文件分交易所存放并按次序取名
def diffExchange(file, count):
   filePath = file + mid_path
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
            if os.path.exists("./" + exchangeName) != True:
               cmd = "mkdir " + exchangeName
               os.system(cmd)
         os.chdir(filePath)
         newName =  fullName + "_" + str(count) + ".csv"
         cmd = "mv " + cfile + " " + newName
         os.system(cmd)

         cmd = "mv " + newName + " ../../../" + exchangeName
         os.system(cmd)
 
   return

#这个函数就是将同一个交易所的105、106这种分类型存放
def diffType():
   dirs = os.listdir(path)
   for file in dirs:
      if os.path.isdir(file) != True:
         continue
      else:
         os.chdir("./" + file)
         mdirs = os.listdir(os.getcwd())
         for mfile in mdirs:
            if os.path.isfile(mfile) != True:
               continue
            else:
               dataType = mfile.split('_', 2)[1]
               if dataType not in typeInfo:
                  typeInfo.append(dataType)

               if os.path.exists("./" + dataType) != True:
                  cmd = "mkdir " + dataType
                  os.system(cmd)
               cmd = "mv " + mfile + " ./" + dataType
               os.system(cmd)

               os.chdir("./" + dataType)
               diffCoin(os.getcwd(), mfile)
               cmd = "rm -rf ./" + mfile
               os.system(cmd)
               os.chdir("../")

      os.chdir("../")
   typeInfo.clear()

   return

#下面这个函数是真正开始将相同币对集中起来
def diffCoin(truePath, filename):
   print(truePath.rsplit('/',1)[1])
   ''''
   dirs = os.listdir(truePath)
   if os.path.exists(filename) != True:
      print("don't exist this file:" + filename)
      return
   flag = 0
   
   for file in dirs:
      if file != filename:
         continue
      elif os.path.getsize(filename) == 0:
         print("this file " + filename + " is empty")
      else:
         outFile = open(filename, 'r')
         csv_file = csv.reader(outFile)
         for row_data in csv_file:
            if flag == 0:
               #saveData = row_data
               flag = 1
               continue
            else:
               newFile = row_data[0] + ".csv"               
               if os.path.exists(newFile) != True:                                 
                  cmd = "touch " + newFile
                  os.system(cmd)
               inFile = open(newFile, 'a', newline='')
               csv_write = csv.writer(inFile, dialect='excel')
               csv_write.writerow(row_data)
               inFile.close()
            flag = 1
         outFile.close()
      '''
   return

#由于105、106、110的文件不一样，不能统一处理
def deal105():
   return

def deal106():
   return

def deal110():
   return

#通过这个main函数来控制函数执行顺序
def main():
   unzipFile()
   diffType()

   #os.system("python /liandao/yjj_data/TK15/bmd/md/deal_data.py")
   return

main()
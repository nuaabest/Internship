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

path = "/liandao/yjj_data/" + sys.argv[1]
mid_path = "/shared/performance_report/data"

exchange = []
coinInfo = []
typeInfo = []

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
         curPath = path# + endFile
         diffExchange(curPath, count)

         count += 1
         os.chdir(path)
         cmd = "rm -rf ./shared"
         os.system(cmd)
   
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
   nowPath = os.getcwd()
   dirs = os.listdir(nowPath)
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
               typeInfo.clear()

               cmd = "mv " + mfile + " ./" + dataType
               os.system(cmd)

      os.chdir("../")
   return

#通过这个main函数来控制函数执行顺序
def main():
   unzipFile()
   diffType()
   #os.system("python /liandao/yjj_data/TK15/bmd/md/deal_data.py")
   return

main()
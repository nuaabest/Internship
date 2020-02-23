#!/usr/bin/python
# *=======================================================*
# -*- coding:utf-8 -*-
# * time :
# * author : lichengyi
# *=======================================================*
# 将iso8601的时间格式转换为unix格式

import os
import datetime
import pytz
import csv
import codecs

file_source = 'C:\\Users\\Administrator\\Desktop\\binance_105.txt'
file_dest = 'C:\\Users\\Administrator\\Desktop\\lichengyi_.txt'

def add_same_price_num():
    input_file = open(file_source, 'r')
    output_file = open(file_dest, 'w')

    line = input_file.readline()
    while line:
        a = line[:-1].split(',')
        #此处得到的a[0]就是人便于观看的时间转换为Unix时间戳
        mid = float(iso2timestamp(a[0], format='%Y-%m-%dT%H:%M:%S.%fZ',timespec='milliseconds'))
        mid_ = float(a[13]) / 1000000
        #mid就是将ISO格式转化为了的Unix时间戳格式，将其写入一个新文件即可
        re = mid - mid_
        re_ = str(re)
        list_ = [str(mid), re_]
        for i in range(len(list_)):
            s = str(list_[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
            if i == 1:
                s = s.replace("'",'').replace(',','') +'\n'  
            else:
                s = s.replace("'",'').replace(',','') +' '   #去除单引号，逗号，每行末尾追加换行符
            output_file.write(s)
        line = input_file.readline()

    
    input_file.close
    output_file.close

    return

def iso2timestamp(datestring, format='%Y-%m-%dT%H:%M:%S.%fZ',timespec='milliseconds'):

    tz = pytz.timezone('Asia/Shanghai')
    utc_time = datetime.datetime.strptime(datestring, format)  # 将字符串读取为 时间 class datetime.datetime

    time = utc_time.replace(tzinfo=pytz.utc).astimezone(tz)

    times = {
        'seconds': int(time.timestamp()),
        'milliseconds': round(time.timestamp() * 1000),
        'microseconds': round(time.timestamp() * 1000 * 1000),
    }
    return times[timespec]
    
add_same_price_num()
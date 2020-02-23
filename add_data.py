# *=======================================================*
# -*- coding:utf-8 -*-
# * time : 2020-02-22 9:47
# * author : lichengyi
# *=======================================================*
# 将相同价格的订单数量加起来
# 本脚本的作用是将相同价格的订单数量相加，分为asks和bids两个部分
# 本思路是当前一次取出的价格和这次取出的价格相同时就将volume相
# 加，如果不同就去存放数据的列表中去查看是否有这个价格存在，不存
# 在就将该加入列表，存在就将volume相加

import os
import json
import string

source_path = 'C:\\Users\\Administrator\\Desktop\\data_test.txt'
save_path = 'C:\\Users\\Administrator\\Desktop\\lichengyi.txt'

def add_data():
    out_file = open(source_path, 'r')
    in_file = open(save_path, 'a')

    asks = []
    bids = []
    #创建两个空列表，用于存放已统计的值
    line = out_file.readline()
    line = line.replace("'", "\"")
    mid_json = json.loads(line)
    
    length_asks = len(mid_json['asks'])
    length_bids = len(mid_json['bids'])
    #count = 0
    asks_pre_price = float(mid_json['asks'][0][1])
    asks_pre_volume = 0
    bids_pre_price = float(mid_json['bids'][0][1])
    bids_pre_volume = 0
    while line:
        #处理asks这一部分的代码，和bids是一样的
        #注意的是因为还需要处理每个列表的最后一个数据，所以范围是0~length_asks
        #当是最后一个数据的时候就直接取出参与后面的运算
        for count_asks in range (length_asks + 1):
            if count_asks == length_asks:
                asks_price = 0
                asks_volume = 0
            else :
                asks_price = float(mid_json['asks'][count_asks][1])
                asks_volume = float(mid_json['asks'][count_asks][2])
            if asks_price == asks_pre_price:
                asks_volume += asks_pre_volume
            #前一次的价格和后一次的价格不一样的时候就表示需要
            else:
                local = if_data_exist(asks_pre_price, asks)
                if local == -1:
                #返回的值是-1表明此时列表中无这个价格的数据，直接添加前一个数据
                    mid = []
                    mid.append(asks_pre_price)
                    mid.append(asks_pre_volume)
                    asks.append(mid)
                else:
                #如果之前在列表中有一个相同的价格，就需要将本来有的加起来
                    asks[local][1] += asks_pre_volume
                
            asks_pre_price = asks_price
            asks_pre_volume = asks_volume

        #处理bids部分的代码
        for count_bids in range (length_bids + 1):
            if count_bids == length_bids:
                bids_price = 0
                bids_volume = 0
            else :
                bids_price = float(mid_json['bids'][count_bids][1])
                bids_volume = float(mid_json['bids'][count_bids][2])
            if bids_price == bids_pre_price:
                bids_volume += bids_pre_volume
            #前一次的价格和后一次的价格不一样的时候就表示需要
            else:
                local = if_data_exist(bids_pre_price, bids)
                if local == -1:
                #返回的值是-1表明此时列表中无这个价格的数据，直接添加前一个数据
                    mid = []
                    mid.append(bids_pre_price)
                    mid.append(bids_pre_volume)
                    bids.append(mid)
                else:
                #如果之前在列表中有一个相同的价格，就需要将本来有的加起来
                    bids[local][1] += bids_pre_volume
                
            bids_pre_price = bids_price
            bids_pre_volume = bids_volume
        
        line = out_file.readline()
        line = line.replace("'", "\"")
        if "\"" in line:
            mid_json = json.loads(line)
    
        length_asks = len(mid_json['asks'])
        length_bids = len(mid_json['bids'])

        asks_pre_price = float(mid_json['asks'][0][1])
        asks_pre_volume = 0
        bids_pre_price = float(mid_json['bids'][0][1])
        bids_pre_volume = 0

    #将asks的列表和bids的列表内容导入新建的文件
    #分为两个部分，asks和bids
    str_asks = "asks"
    in_file.writelines(str_asks+'\n')
    length_asks = len(asks)
    asks.sort()
    for count in range(length_asks):
        in_file.writelines(str(asks[count][0])+' '+str(asks[count][1])+'\n')
    
    str_bids = "bids"
    in_file.writelines('\n'+str_bids+'\n')
    length_bids = len(bids)
    bids.sort()
    for count in range(length_bids):
        in_file.writelines(str(bids[count][0])+' '+str(bids[count][1])+'\n')

    out_file.close()
    in_file.close()

    return 

#这个函数就是判断该价格是否存在于列表中，如果存入过就返回存入的位置
def if_data_exist(price, li=[]):
    length = len(li)
    for i in range(length):
        if price == li[i][0]:
            return i
    return -1

add_data()
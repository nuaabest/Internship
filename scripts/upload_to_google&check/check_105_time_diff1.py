import os
import sys
import csv
import datetime
import codecs
import json
import numpy as np
import matplotlib.pyplot as pyplot
np.set_printoptions(suppress = True)

if len(sys.argv) != 3:
    print('command like: python3 {} 2020-02-28 [server name]'.format(sys.argv[0]))
    sys.exit(1)
    
date = sys.argv[1] + '105'
#time = sys.argv[2]
currntPath = os.getcwd()
outputPath105 = os.path.join(currntPath, date)
date = sys.argv[1] + '106'
outputPath106 = os.path.join(currntPath, date)

if not os.path.exists(outputPath105):
    os.makedirs(outputPath105)
if not os.path.exists(outputPath106):
    os.makedirs(outputPath106)

def cal_data(y_series, result, flag):
    a = sorted(y_series)
    if flag == 1:
        result['90%Percentile'] = '-'
        result['median'] = '-'
        result['mean'] = '-'
        result['max'] = '-'
        result['min'] = '-'
        result['variance'] = '-'
        result['std'] = '-'
    else:        
        result['90%Percentile'] = np.percentile(a, 90)
        result['median'] = np.median(a)
        result['mean'] = np.mean(a)
        result['max'] = np.max(a)
        result['min'] = np.min(a)
        result['variance'] = np.var(a)
        result['std'] = np.std(a, ddof = 1)

result105 = {}
result106 = {}
config = {}

serverName = sys.argv[2]
if serverName == 'TK15':
    with open("/liandao/lcy-scripts/configTK15.json") as config_file:
        config = json.load(config_file)
        config = config['exchanges']
elif serverName == 'IRL-Deribit':
    with open("/liandao/lcy-scripts/configIRL.json") as config_file:
        config = json.load(config_file)
        config = config['exchanges']
else:
    with open("/liandao/lcy-scripts/configTK10.json") as config_file:
        config = json.load(config_file)
        config = config['exchanges']

for name,values in config.items():
    #此时已经进入了/liandao/yjj_data/[docker]/[日期]文件夹下
    #有这个docker收的数据的交易所的名称
    os.chdir(name)
    os.chdir('trade')
    files105 = os.listdir(os.getcwd())
    files105.sort(reverse = False)
    pairs105 = len(files105)
    print(name + ': the coin-pairs number about 105 is : ' + str(pairs105))
    
    result105[name] = {}
    result105[name]['actual_pairs_count'] = pairs105
    result105[name]['theo_pairs_count'] = values['pairs_count'] if 'pairs_count' in values else 0
    result105[name]['pairs'] = []
    for file in files105:
        print(file)
        coin_pair = file.split('.')[0]
        result105[name]['pairs'].append(coin_pair)
        #获取当前的这个币对，并放进所有币对的列表
        csvfile105 = open(file, 'r')
        readCSV105 = csv.reader(csvfile105)

        onePairs105 = {}
        onePairs105['X'] = []
        onePairs105['Y'] = []
        #在单币对的这个字典中创建两个列表，一个存放本地时间戳
        #另一个存放本地和交易所的时间戳的差值
        lines = 0
        for row in readCSV105:
            lines += 1
            if lines == 1 :
                continue
            exchange_time = float(row[-9]) / 1000000
            local_time = float(row[-7]) / 1000000
            onePairs105['X'].append(local_time)
            onePairs105['Y'].append(local_time - exchange_time)
        if lines == 1:
            flag = 1 
        else:
            flag = 0
        result105[name][coin_pair] = {}
        cal_data(onePairs105['Y'], result105[name][coin_pair], flag)
        #fig = pyplot.figure(coin_pair)
        #pyplot.scatter(onePairs['X'], onePairs['Y'], s = 0.5)
        #单个币对的图像暂时不进行制作

    os.chdir('../book')
    files106 = os.listdir(os.getcwd())
    files105.sort(reverse = False)
    pairs106 = len(files106)
    print(name + ': the coin-pairs number about 106 is : ' + str(pairs106))
    
    result106[name] = {}
    result106[name]['actual_pairs_count'] = pairs106
    result106[name]['theo_pairs_count'] = values['pairs_count'] if 'pairs_count' in values else 0
    result106[name]['pairs'] = []
    for file in files106:
        print(file)
        breaktimes = 0
        coin_pair = file.split('.')[0]
        result106[name]['pairs'].append(coin_pair)
        #获取当前的这个币对，并放进所有币对的列表
        csvfile106 = open(file, 'r')
        readCSV106 = csv.reader(csvfile106)

        timeDifference = []
        lines = 0
        ptime = 0.0
        ntime = 0.0
        for row in readCSV106:
            lines += 1
            if lines == 1:
                continue
            if lines == 2:
                ptime = float(row[-7]) / 1000000
            if lines > 2:
                ntime = float(row[-7]) / 1000000
                breakTime = ntime - ptime
                if breakTime > 10000:
                    breaktimes += 1
                elif breakTime < 0:
                    print("data concordance error")
                    sys.exit()
                timeDifference.append(breakTime)
                ptime = ntime
        if lines <= 2:
            flag = 1
        else:
            flag = 0
        result106[name][coin_pair] = {}
        cal_data(timeDifference, result106[name][coin_pair], flag)
        result106[name][coin_pair]['breaktimes'] = breaktimes

    os.chdir('../..')

outputfile105 = os.path.join(outputPath105, 'exchanges_{}.json'.format(date))
outputfile106 = os.path.join(outputPath106, 'exchanges_{}.json'.format(date))
with open(outputfile105, 'w') as out_file105:
    json.dump(result105, out_file105)
with open(outputfile106, 'w') as out_file106:
    json.dump(result106, out_file106)

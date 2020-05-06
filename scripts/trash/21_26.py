import datetime
import os
import sys
import shutil

path = 'D:/dataFromBeijing'
'''
now = datetime.datetime.now()
delta = datetime.timedelta(1)
now -= delta

os.chdir(path)
for i in range(0, 6):
    now -= delta
    timestr = now.strftime('%Y-%m-%d')
    files = os.listdir(os.getcwd())
    for file in files:
        if timestr in file:
            datePath = './' + exchange + '/' +timestr
            exchange = file.split('-', 3)[3].split('-', 1)[0]
            if os.path.exists(exchange) != True:
                os.mkdir(exchange)
            else:
                if os.path.exists(datePath) != True:
                    os.mkdir(datePath)
            shutil.move(file, datePath)
'''
result = 1 if 'ing' not in path else 10
print(result)
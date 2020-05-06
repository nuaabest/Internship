import os
import datetime
import sys
import shutil

path = 'D:/dataFromBeijing'

now = datetime.datetime.now()
delta34 = datetime.timedelta(34)
now -= delta34

delta = datetime.timedelta(1)
for i in range(0,24):
    now -= delta
    timestr = now.strftime('%Y%m%d')
    
    try:
        os.chdir('./timestr')
        files = os.listdir(os.getcwd())
        for file in files:
            exchange = file.split('-', 3)[3].split('-', 1)[0]
            if os.path.exists(exchange) != True:
                os.mkdir(exchange)
        shutil.move(file, exchange)  
    except Exception as error:
        print(error)

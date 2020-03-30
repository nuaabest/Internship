#coding:utf-8
#commit yjj_data to beijing

import os

uploading_path = "/shared/performance_report/up_load/up_loading.txt"
file_path = "/shared/performance_report/up_load/"

def commit_data_to_Beijing():
    #up_loading.txt文件存在的时候就说明没有文件或者正在上传一个文件,直接退出
    if_txt_exist = os.path.exists(uploading_path)
    if if_txt_exist == True:
        print("No zip to commit or loading")
        os.sys.exit() 
    #如果没有up_loading.txt文件，先判断一下是否存在.zip文件，存在就
    #挑选存在时间最长的上传  
    #获取到这个目录下的所有文件，然后查看是否存在.zip文件
    else :
        all_files = os.listdir(file_path)
        all_files = sorted(all_files,  key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
        
        length = len(all_files)
        if length == 0:
            print("no zip to commit")
            os.sys.exit()
        else :
            oldest_zip = all_files[0]
            local = file_path + oldest_zip
            print(local)
            remote = "/liandao/yjj_data/TK15/md"
            #oldest_zip就是存在的最长时间的压缩包
            #一旦有压缩包需要上传就创建up_loading.txt文件来确保不会有其他压缩包一起上传

            cmd = "touch " + uploading_path
            os.system(cmd)

            cmd = "expect /shared/util_scripts/crontab_upload_data.sh " + local + " " + remote
            os.system(cmd)
            
			cmd = "expect /shared/ifExist.exp lbc@111.198.66.50 " + remote "/" +  oldest_zip
			flag = os.system(cmd)
			if flag == False:
				cmd = "rm -rf " + local
				os.system(cmd)
				print("not upload::" + cmd)

            cmd = "rm -rf " + uploading_path
            os.system(cmd)

commit_data_to_Beijing()

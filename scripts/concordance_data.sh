# !/bin/bash
# -*- coding:utf-8 -*-
path="/liandao/yjj_data/"$1
function unzipFile()
{
    echo "lichengyi"
    cd ${path}
    echo ${path}
    if [! -d ${path}]
    then
        echo "don't have data in this day"
    else
        for zip_file in 'ls path -t'
        do
            mid=0
            shared="shared_"$mid
            unzip -o -d ./${shared} ${zip_file}
        done
    fi
}

unzipFile

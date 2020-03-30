# !/bin/bash
# *=======================================================*
# -*- coding:utf-8 -*-
# * time : 2020-03-26 16:00
# * author : lichengyi
# *=======================================================*
# send mail if upload fail
nowtime=`date +%M`
day=`date +%Y-%m-%d`
declare -i accurateTime=`date +%H%M`

function judge()
{
    #在00、30时刻正在开始上传，此时不能判断是否丢失
    if [ $nowtime != "30" -a $nowtime != "00" ]
    then
        for file in `ls $1 -t`
        do
            declare -i first=${file:9:4}
            re=`expr $accurateTime - $first`
            if [ re -gt 30 ]
            then
                python /liandao/lcy-concordance-data/sendMail.py $1$file
            fi
            echo "this is legal"
            break
        done     
    fi
}

judge /liandao/yjj_data/TK15/md/
judge /liandao/yjj_data/TK10/lh_strat/
judge /liandao/yjj_data/IRL-Deribit/md/
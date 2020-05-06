# !/bin/bash
# *=======================================================*
# -*- coding:utf-8 -*-
# * time : 2020-03-26 9:34
# * author : lichengyi
# *=======================================================*
# concordance data
preday=$1
predayF=$2

path='liandao/yjj_data'
targetPath='liandao/yjj_md_data'
scripts='liandao/lcy-scripts'

function concordanceData()
{
    echo "tsmc1942" | sudo -S mkdir /$path/$1/$preday

    echo "tsmc1942" | sudo -S mv /$path/$1/$predayF* /$path/$1/$preday

    echo "tsmc1942" | sudo -S python3 /$scripts/concordance_data_lbc.py $2

    echo "tsmc1942" | sudo -S python3 /$scripts/combine.py $2 $3
 
    cd /$path/$1
 
    echo "tsmc1942" | sudo -S python3 /$scripts/check_105_time_diff1.py $preday $3 

    echo "tsmc1942" | sudo -S python3 /$scripts/mail.py $preday 105 $3

    echo "tsmc1942" | sudo -S python3 /$scripts/mail.py $preday 106 $3

    echo "tsmc1942" | sudo -S zip -r /$path/$1/$3"-"$preday".zip" /$path/$1/$preday -x *.zip

    echo "tsmc1942" | sudo -S mv /$path/$1/$3"-"$preday".zip" /$targetPath/$3

    rmPath=/$path/$1/$preday
    for file in `ls $rmPath`
    do
        if [ -d $rmPath/$file ]
        then
            echo "tsmc1942" | sudo -S rm -rf $rmPath/$file
        fi
    done
}

concordanceData TK15/md TK15/md/${preday} TK15
concordanceData IRL-Deribit/md IRL-Deribit/md/${preday} IRL-Deribit
concordanceData TK10/lh_strat TK10/lh_strat/${preday} TK10

# !/bin/bash
# *=======================================================*
# -*- coding:utf-8 -*-
# * time : 2020-03-26 9:34
# * author : lichengyi
# *=======================================================*
# concordance data
preday=`date -d "-1 days" +%Y-%m-%d`
predayF=`date -d "-1 days" +%Y%m%d`

path='liandao/yjj_data'
targetPath='liandao/yjj_md_data'
scripts='liandao/lcy-scripts'

function concordanceData()
{
    echo "1999nyc" | sudo -S mkdir /$path/$1/$preday

    echo "1999nyc" | sudo -S mv /$path/$1/$predayF* /$path/$1/$preday

    echo "1999nyc" | sudo -S python3 /$scripts/concordance_data.py $2

    echo "1999nyc" | sudo -S python3 /$scripts/combine.py $2

    echo "1999nyc" | sudo -S zip -r /$path/$1/$3"-"$preday".zip" /$path/$1/$preday -x *.zip

    echo "1999nyc" | sudo -S mv /$path/$1/$3"-"$preday".zip" /$targetPath/$3

    rmPath=/$path/$1/$preday
    for file in `ls $rmPath`
    do
        if [ -d $rmPath/$file ]
        then
            rm -rf $rmPath/$file
        fi
    done
}

concordanceData TK15/md TK15/md/${preday} TK15
concordanceData IRL-Deribit/md IRL-Deribit/md/${preday} IRL-Deribit
concordanceData TK10/lh_strat TK10/lh_strat/${preday} TK10
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
scripts='liandao/lcy-concordance-data'

function concordanceData()
{
    echo "1999nyc" | sudo -S mkdir /$path/$1/$preday

    echo "1999nyc" | sudo -S mv /$path/$1/$predayF* /$path/$1/$preday

    echo "1999nyc" | sudo -S python3 /$scripts/concordance_data.py $2

    echo "1999nyc" | sudo -S python3 /$scripts/combine.py $2

    echo "1999nyc" | sudo -S zip -r /$path/$1/$preday".zip" /$path/$1/$preday -x *.zip

    echo "1999nyc" | sudo -S mv /$path/$1/$preday".zip" /$targetPath
}

concordanceData TK15/bmd/md TK15/md/${preday}
concordanceData IRL-Deribit/md IRL-Deribit/md/${preday}
concordanceData TK10/lh_strat TK10/lh_strat/${preday} 
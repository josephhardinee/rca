#!/bin/bash
#PBS -A arm
#PBS -N mar_csapr_ppi
#PBS -l nodes=16:ppn=16
#PBS -l walltime=02:00:00
#PBS -l qos=std
#PBS -W group_list=cades-arm
#PBS -q arm_high_mem
#PBS -j oe
#PBS -m abe
#PBS -M alexis.hunzinger@pnnl.gov
#PBS -o o.log
#PBS -e e.log
#PBS -S /bin/bash

#array=( 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31)
#array=( 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 )
#array=( 19 20 21 22 23 24 25 26 27 28 29 30 31)
array=( 01 02 03 )
for u in "${array[@]}"
do
    python /home/alexishunzinger/projects/taranis/taranis/calibration/daily_rca_ppi.py /home/alexishunzinger/data/proj-shared/data_transfer/cor/corcsapr2cfrppiM1.a1/ cor csapr2 201903"$u" /home/alexishunzinger/projects/taranis/taranis/calibration/datafiles/ /home/alexishunzinger/projects/taranis/taranis/calibration/datafiles/ 20181108 composite /home/alexishunzinger/projects/taranis/taranis/calibration/datafiles/
done

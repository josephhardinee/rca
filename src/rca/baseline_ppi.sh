#!/bin/bash
#PBS -A arm
#PBS -N corcsapr_ppi
#PBS -l nodes=16:ppn=16
#PBS -l walltime=02:00:00
#PBS -W group_list=cades-arm
#PBS -q arm_high_mem
#PBS -j oe
#PBS -m abe
#PBS -M alexis.hunzinger@pnnl.gov
#PBS -o o.log
#PBS -e e.log
#PBS -S /bin/bash


python /home/alexishunzinger/projects/taranis/taranis/calibration/baseline_ppi.py /home/alexishunzinger/data/proj-shared/data_transfer/cor/corcsapr2cfrppiM1.a1/ cor csapr2 20181108 /home/alexishunzinger/projects/taranis/taranis/calibration/datafiles/ /home/alexishunzinger/projects/taranis/taranis/calibration/datafiles/

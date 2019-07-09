#!/bin/bash
#PBS -A arm
#PBS -N corxsapr_0508
#PBS -q arm_high_mem
#PBS -l nodes=8:ppn=16
#PBS -l qos=std
#PBS -l walltime=01:00:00
#PBS -W group_list=cades-arm
#PBS -j oe
#PBS -m abe
#PBS -M alexis.hunzinger@pnnl.gov
#PBS -o o.log
#PBS -e e.log
#PBS -S /bin/bash


#python /home/alexishunzinger/projects/taranis/taranis/calibration/clutter_map_ppi.py /home/alexishunzinger/data/proj-shared/data_transfer/cor/corkasacrcfrppivM1.a1/ cor kasacr 20190314 /home/alexishunzinger/projects/taranis/taranis/calibration/

python /home/alexishunzinger/projects/taranis/taranis/calibration/clutter_map_ppi.py /home/alexishunzinger/projects/sgp/sgpxsaprppiI5.00/ sgp xsaprI5 20110508 /home/alexishunzinger/projects/taranis/taranis/calibration/

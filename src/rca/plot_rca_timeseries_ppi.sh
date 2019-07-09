#!/bin/bash
#PBS -A arm
#PBS -N timeseries
#PBS -l nodes=2:ppn=16
#PBS -l walltime=00:02:00
#PBS -l qos=std
#PBS -W group_list=cades-arm
#PBS -q arm_high_mem
#PBS -j oe
#PBS -m abe
#PBS -M alexis.hunzinger@pnnl.gov
#PBS -o o.log
#PBS -e e.log
#PBS -S /bin/bash

python /home/alexishunzinger/projects/taranis/taranis/calibration/plot_rca_timeseries_ppi.py /home/alexishunzinger/projects/taranis/taranis/calibration/ /home/alexishunzinger/projects/taranis/taranis/calibration/figures/ sgp xsaprI5 SGPXSAPRI5 2011-04-30


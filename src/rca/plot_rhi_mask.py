#!/usr/bin/env python
import matplotlib.pyplot as plt
import pyart
import numpy as np
import os
import glob

#filename = ['/home/alexishunzinger/data/proj-shared/data_transfer/cor/corcsapr2cfrhsrhiM1.a1/corcsapr2cfrhsrhiM1.a1.20190315.111803.nc.v0']#,'/home/alexishunzinger/data/proj-shared/data_transfer/cor/corcsapr2cfrhsrhiM1.a1/corcsapr2cfrhsrhiM1.a1.20190315.010642.nc.v0']
filepath = '/home/alexishunzinger/data/proj-shared/data_transfer/cor/corcsapr2cfrhsrhiM1.a1/'
for f in glob.glob(os.path.join(filepath,'*csapr2*20190315.1*.??')):
#for f in filename:
    print(f)
  
    radar = pyart.io.cfradial.read_cfradial(f, file_field_names=True)
    xlim = [-90,90]
    ylim = [0,18]
    radar.azimuth['data'][:] = 270.0
    radar.init_gate_x_y_z()
    elev = radar.elevation['data']
    theta = radar.azimuth['data']
    start = radar.sweep_start_ray_index['data'][0]
    end = radar.sweep_end_ray_index['data'][0]+1
    zh = radar.fields['attenuation_corrected_reflectivity_h']['data'][start:end,:].data
    ve = radar.fields['mean_doppler_velocity']['data'][start:end,:].data
    nanidx_low = elev < 1.0
    nanidx_hi = elev > 179.0
    nanidx = np.logical_or(nanidx_low,nanidx_hi)
    zh[nanidx,:] = np.nan
    ve[nanidx,:] = np.nan
    radar.add_field_like('attenuation_corrected_reflectivity_h','reflectivity_mod',zh)
    radar.add_field_like('mean_doppler_velocity','mean_doppler_velocity_mod',ve)

    display = pyart.graph.RadarDisplay(radar)
    fig = plt.figure(figsize=[10, 4])
    ax = fig.add_subplot(111)
    display.plot_rhi('reflectivity_mod', 0, vmin=-15.0, vmax=60.0, cmap='pyart_NWSRef',gatefilter=None)#jet
    display.set_limits(xlim=xlim,ylim=ylim)
    plt.savefig('/home/alexishunzinger/projects/taranis/taranis/calibration/figures/mrhi/zh/csapr2_mrhi_zh_20190315_'+f[112:118]+'.png')
    plt.close()

    fig = plt.figure(figsize=[10, 4])
    ax = fig.add_subplot(111)
    display.plot_rhi('mean_doppler_velocity_mod', 0, vmin=-16.5, vmax=16.5, cmap='seismic', gatefilter=None, filter_transitions=False)
    display.set_limits(xlim=xlim,ylim=ylim)
    plt.savefig('/home/alexishunzinger/projects/taranis/taranis/calibration/figures/mrhi/ve/csapr2_mrhi_ve_20190315_'+f[112:118]+'.png')
    plt.close()




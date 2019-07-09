#!/usr/bin/env python
import sys
import numpy as np
import pyart
import os
import glob
#import pandas as pd
from netCDF4 import Dataset 
from matplotlib.pyplot import cm
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(
            "ERROR: Arguments are file directory, site, instrument, date"
        )
        sys.exit(0)

    filedir = sys.argv[1]
    site = sys.argv[2]
    inst = sys.argv[3]
    date = sys.argv[4]

    bins_h = []
    bins_v = []
    pdf_h = []
    pdf_v = []
    cdf_h = []
    cdf_v = []
    d95_h = []
    d95_v = []
    time = []

    for f in glob.glob(os.path.join(filedir, 'pdf*'+site+inst+'_'+date+'*.nc')):
        dataset = Dataset(f)
        time.append(f[-11:-4]) 
        bins_h.append(dataset.variables['bin_zh'][:])
        bins_v.append(dataset.variables['bin_zv'][:])
        pdf_h.append(dataset.variables['pdf_zh'][:])
        pdf_v.append(dataset.variables['pdf_zv'][:])
        cdf_h.append(dataset.variables['cdf_zh'][:])
        cdf_v.append(dataset.variables['cdf_zv'][:])
        d95_h.append(dataset.variables['dbz95_zh'][:])
        d95_v.append(dataset.variables['dbz95_zv'][:])
        dataset.close()

    # Sort by time
    time = np.array(time)
    bins_h = np.array(bins_h)
    bins_v = np.array(bins_v)
    pdf_h = np.array(pdf_h)
    pdf_v = np.array(pdf_v)
    cdf_h = np.array(cdf_h)
    cdf_v = np.array(cdf_v)

    idx = np.argsort(time)
    time_sort = time[idx]
    bins_h_sort = bins_h[idx]
    bins_v_sort = bins_v[idx]
    pdf_h_sort = pdf_h[idx]
    pdf_v_sort = pdf_v[idx]
    cdf_h_sort = cdf_h[idx]
    cdf_v_sort = cdf_v[idx]

    interval = 10
    time_hr = time_sort[::10]
    bins_h_hr = bins_h_sort[::10]
    bins_v_hr = bins_v_sort[::10]
    pdf_h_hr = pdf_h_sort[::10]
    pdf_v_hr = pdf_v_sort[::10]
    cdf_h_hr = cdf_h_sort[::10]
    cdf_v_hr = cdf_v_sort[::10]

    plt.style.use('publication')

    size = 9
    family = 'sans'
    color=iter(cm.gist_yarg(np.linspace(0,1,len(time_hr))))

    # Begin plotting
    fig, ax = plt.subplots()#figsize=[8,4])
    ax.axhline(95.,linestyle='--',color='grey')
    ax.axvline(np.nanmedian(d95_h),linestyle='--',color='grey')
    ax.set_ylabel('PDF*2 and CDF (%)')
    ax.set_title('PDF / CDF of clutter area reflectivity \n ENA XSAPR2 2018-01-25')
    ax.set_xlabel('Reflectivity (dBZ)')
    locs, labs = plt.xticks()
    # plt.xticks(locs[::7])
    plt.xticks
    #plt.gcf().autofmt_xdate()
    axins = zoomed_inset_axes(ax, 8.5, bbox_to_anchor=(200, 300), loc='center left') # zoom-factor: 2.5, location: upper-left
    axins.axhline(95.,linestyle='--',color='grey')
    axins.axvline(np.nanmedian(d95_h),linestyle='--',color='grey')
    mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")

    for idx in range(0,len(time_hr)):
        c = next(color)
        ax.plot(bins_h_hr[idx][1:],pdf_h_hr[idx]*2,color=c)
        ax.plot(bins_h_hr[idx][1:],cdf_h_hr[idx],color=c)
        axins.plot(bins_h_hr[idx][1:],pdf_h_hr[idx]*2,color=c)
        axins.plot(bins_h_hr[idx][1:],cdf_h_hr[idx],color=c)

        x1, x2, y1, y2 = 54, 57, 93, 97 # specify the limits
        axins.set_xlim(x1, x2) # apply the x-limits
        axins.set_ylim(y1, y2) # apply the y-limits

        

    plt.savefig(filedir+'pdf_enaxsapr2_20180125.png')
    print(np.nanmedian(d95_h))
    # Done plottinh

    # ax.axhline(0.,linestyle='--',color='grey')
    # ax.scatter(df['DATE'],df['RCA_H'],
    #            color='k',
    #            linewidth=lw)
    # ax.plot(df['DATE'],df['RCA_H'],
    #            color='k',
    #            linewidth=lw)
    # ax.set_ylabel('RCA value')
    # ax.set_title('Daily RCA values (H) at '+location+' \n RHI')
    # ax.set_ylim(ylim)
    # ax.scatter(baseline,0.0,marker='D',linewidth=lww,color='b')
    # ax.text(xtext0,ytext,h_text,size=size,family=family)
    # locs, labs = plt.xticks()
    # plt.xticks(locs[::7])
    # plt.xticks
    # plt.gcf().autofmt_xdate()
    # plt.savefig(fig_outpath+'rca_h_hsrhi_'+site+inst+'.png')


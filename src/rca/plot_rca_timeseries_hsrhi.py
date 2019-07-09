#!/usr/bin/env python
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print(
            "ERROR: Arguments are csv file path, output path for figures, site, instrument, location, baseline date"
        )
        sys.exit(0)

    csvpath = sys.argv[1]
    fig_outpath = sys.argv[2]
    site = sys.argv[3]
    inst = sys.argv[4]
    location = sys.argv[5]
    baseline = sys.argv[6]
    print(csvpath, fig_outpath, site, inst, baseline)

#plt.style.use('seaborn-paper')
#plt.style.use('ggplot')
plt.style.use('publication')
params = {'mathtext.default': 'regular' }          
plt.rcParams.update(params)

#location = 'COR CSAPR2'
#csvfile = csvpath+'daily_rcavalues_hsrhi_'+site+inst+'.csv'
csvfile = csvpath+'daily_rcavalues_hsrhi_'+site+inst+'_march.csv'

# Change text box locations as needed
ylim = -2.0,4.0
lw = 0.5
lww = 1.0
ytext = -1. #0.5 
xtext = 24.0
xtext0 = 18.0

size = 9
family = 'sans'

df = pd.read_csv(csvfile)
df = df.sort_values(by='DATE')

if inst == 'kasacr':
    # Calculate mean, standard deviation, minimum value, and maximum of RCA values
    h_mean = str(np.nanmean(df['RCA_H']))[0:5]
    h_std = str(np.nanstd(df['RCA_H'],ddof=1))[0:5]
    h_min = str(min(df['RCA_H']))[0:5]
    h_max = str(max(df['RCA_H']))[0:5]

    h_text = ' \n Mean: '+h_mean+' \n StDev: '+h_std+' \n Min: '+h_min+' \n Max: '+h_max+''
    h = 'H \n Mean: '+h_mean+' \n StDev: '+h_std+' \n Min: '+h_min+' \n Max: '+h_max+''

    # Plot the H polarization RCA values only
    fig, ax = plt.subplots()#figsize=[8,4])
    ax.axhline(0.,linestyle='--',color='grey')
    ax.scatter(df['DATE'],df['RCA_H'],
               color='k',
               linewidth=lw)
    ax.plot(df['DATE'],df['RCA_H'],
               color='k',
               linewidth=lw)
    ax.set_ylabel('RCA value')
    ax.set_title('Daily RCA values (H) at '+location+' \n RHI')
    ax.set_ylim(ylim)
    ax.scatter(baseline,0.0,marker='D',linewidth=lww,color='b')
    ax.text(xtext0,ytext,h_text,size=size,family=family)
    locs, labs = plt.xticks()
    plt.xticks(locs[::7])
    plt.xticks
    plt.gcf().autofmt_xdate()
    plt.savefig(fig_outpath+'rca_h_hsrhi_'+site+inst+'_march.png')


else:
    # Calculate mean, standard deviation, minimum value, and maximum of RCA values
    h_mean = str(np.nanmean(df['RCA_H']))[0:5]
    v_mean = str(np.nanmean(df['RCA_V']))[0:5]
    h_std = str(np.nanstd(df['RCA_H'],ddof=1))[0:5]
    v_std = str(np.nanstd(df['RCA_V'],ddof=1))[0:5]
    h_min = str(min(df['RCA_H']))[0:5]
    v_min = str(min(df['RCA_V']))[0:5]
    h_max = str(max(df['RCA_H']))[0:5]
    v_max = str(max(df['RCA_V']))[0:5]

    h_text = ' \n Mean: '+h_mean+' \n StDev: '+h_std+' \n Min: '+h_min+' \n Max: '+h_max+''
    v_text = ' \n Mean: '+v_mean+' \n StDev: '+v_std+' \n Min: '+v_min+' \n Max: '+v_max+''
    h = 'H \n Mean: '+h_mean+' \n StDev: '+h_std+' \n Min: '+h_min+' \n Max: '+h_max+''
    v = 'V \n Mean: '+v_mean+' \n StDev: '+v_std+' \n Min: '+v_min+' \n Max: '+v_max+''

    # Plot the H polarization RCA values only
    fig, ax = plt.subplots()#figsize=[8,4])
    ax.axhline(0.,linestyle='--',color='grey')
    ax.scatter(df['DATE'],df['RCA_H'],
                color='k',
                linewidth=lw)
    ax.plot(df['DATE'],df['RCA_H'],
                color='k',
                linewidth=lw)
    ax.set_ylabel('RCA value')
    ax.set_title('Daily RCA values (H) at '+location+' \n RHI')
    ax.set_ylim(ylim)
    ax.scatter(baseline,0.0,marker='D',linewidth=lww,color='b')
    ax.text(xtext0,ytext,h_text,size=size,family=family)
    locs, labs = plt.xticks()
    plt.xticks(locs[::7])
    plt.xticks
    plt.gcf().autofmt_xdate()
    plt.savefig(fig_outpath+'rca_h_hsrhi_'+site+inst+'.png')

    # Plot the V polarization RCA values only
    fig, ax = plt.subplots()#figsize=[8,4])
    ax.axhline(0.,linestyle='--',color='grey')
    ax.scatter(df['DATE'],df['RCA_V'],
                color='k',
                linewidth=lw)
    ax.plot(df['DATE'],df['RCA_V'],
                color='k',
                linewidth=lw)
    ax.set_ylabel('RCA value')
    ax.set_title('Daily RCA values (V) at '+location+' \n RHI')
    ax.set_ylim(ylim)
    ax.scatter(baseline,0.0,marker='D',linewidth=lww,color='b')
    ax.text(xtext0,ytext,v_text,size=size,family=family)
    locs, labs = plt.xticks()
    plt.xticks(locs[::7])
    plt.xticks
    plt.gcf().autofmt_xdate()
    plt.savefig(fig_outpath+'rca_v_hsrhi_'+site+inst+'.png')

    # Plot the H and V polarization RCA values together
    fig, ax = plt.subplots()#figsize=[8,4])
    ax.axhline(0.,linestyle='--',color='grey')
    ax.scatter(df['DATE'],df['RCA_H'],
                color='k',
                linewidth=lw,
                label='H')
    ax.plot(df['DATE'],df['RCA_H'],
                color='k',
                linewidth=lw,
                label='')
    ax.scatter(df['DATE'],df['RCA_V'],
                color='slategrey',
                linewidth=lw,
                label='V')
    ax.plot(df['DATE'],df['RCA_V'],
                color='slategrey',
                linewidth=lw,
                label='')
    ax.legend()
    ax.set_ylabel('RCA value')
    ax.set_title('Daily RCA values at '+location+' \n RHI')
    ax.set_ylim(ylim)
    ax.scatter(baseline,0.0,marker='D',linewidth=lww,color='b')
    ax.text(xtext0,ytext,h,size=size,family=family)
    ax.text(xtext,ytext,v,size=size,family=family)
    locs, labs = plt.xticks() 
    plt.xticks(locs[::7]) 
    plt.xticks
    plt.gcf().autofmt_xdate()
    plt.savefig(fig_outpath+'rca_hv_hsrhi_'+site+inst+'.png')

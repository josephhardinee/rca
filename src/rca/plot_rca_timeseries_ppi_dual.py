#!/usr/bin/env python
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import string

if __name__ == "__main__":
    if len(sys.argv) < 8:
        print(
            "ERROR: Arguments are csv file path, output path for figures, site, instrument, location, baseline date1,  baseline date2"
        )
        sys.exit(0)

    csvpath = sys.argv[1]
    fig_outpath = sys.argv[2]
    site = sys.argv[3]
    inst = sys.argv[4]
    location = sys.argv[5]
    baseline1 = sys.argv[6]
    baseline2 = sys.argv[7]
    print(csvpath, fig_outpath, site, inst, baseline1, baseline2)

plt.style.use('publication')
params = {'mathtext.default': 'regular' }          
plt.rcParams.update(params)

csvfile1 = csvpath+'daily_rcavalues_ppi_'+site+inst+'_0313.csv'
csvfile2 = csvpath+'daily_rcavalues_ppi_'+site+inst+'.csv'

# Change text box locations as needed
ylim = -5.0,5.0
lw = 0.5
lww = 1.0
ytext = 2.0
xtext = 8.0
xtext0 = 8.0

locationstr = location[0:3]+' '+location[3:]

size = 11
family = 'sans'

df1 = pd.read_csv(csvfile1)
# Ensure values in csv file are in chronological order
df1 = df1.sort_values(by='DATE')
df2 = pd.read_csv(csvfile2)
# Ensure values in csv file are in chronological order
df2 = df2.sort_values(by='DATE')

if inst == 'kasacr':
    print('kasacr')
else:
    # Calculate mean, standard deviation, minimum value, and maximum of RCA values
    h_mean1 = str(np.nanmean(df1['RCA_H']))[0:5]
    v_mean1 = str(np.nanmean(df1['RCA_V']))[0:5]
    h_std1 = str(np.nanstd(df1['RCA_H'],ddof=1))[0:5]
    v_std1 = str(np.nanstd(df1['RCA_V'],ddof=1))[0:5]
    h_min1 = str(min(df1['RCA_H']))[0:5]
    v_min1 = str(min(df1['RCA_V']))[0:5]
    h_max1 = str(max(df1['RCA_H']))[0:5]
    v_max1 = str(max(df1['RCA_V']))[0:5]

    h_text1 = ' \n Mean:  '+h_mean1+' \n StDev: '+h_std1+' \n Min:    '+h_min1+' \n Max:    '+h_max1+''
    v_text1 = ' \n Mean:  '+v_mean1+' \n StDev: '+v_std1+' \n Min:    '+v_min1+' \n Max:    '+v_max1+''
    h1 = 'H \n Mean:  '+h_mean1+' \n StDev: '+h_std1+' \n Min:    '+h_min1+' \n Max:    '+h_max1+''
    v1 = 'V \n Mean:  '+v_mean1+' \n StDev: '+v_std1+' \n Min:    '+v_min1+' \n Max:    '+v_max1+''

    h_mean2 = str(np.nanmean(df2['RCA_H']))[0:5]
    v_mean2 = str(np.nanmean(df2['RCA_V']))[0:5]
    h_std2 = str(np.nanstd(df2['RCA_H'],ddof=1))[0:5]
    v_std2 = str(np.nanstd(df2['RCA_V'],ddof=1))[0:5]
    h_min2 = str(min(df2['RCA_H']))[0:5]
    v_min2 = str(min(df2['RCA_V']))[0:5]
    h_max2 = str(max(df2['RCA_H']))[0:5]
    v_max2 = str(max(df2['RCA_V']))[0:5]

    h_text2 = ' \n Mean:  '+h_mean2+' \n StDev: '+h_std2+' \n Min:    '+h_min2+' \n Max:    '+h_max2+''
    v_text2 = ' \n Mean:  '+v_mean2+' \n StDev: '+v_std2+' \n Min:    '+v_min2+' \n Max:    '+v_max2+''
    h2 = 'H \n Mean:  '+h_mean2+' \n StDev: '+h_std2+' \n Min:    '+h_min2+' \n Max:    '+h_max2+''
    v2 = 'V \n Mean:  '+v_mean2+' \n StDev: '+v_std2+' \n Min:    '+v_min2+' \n Max:    '+v_max2+''

    fig, axes = plt.subplots(nrows=2,ncols=1,sharex=True,
                            figsize=[10,10])
    # Plot the H polarization RCA values only
    #fig, ax = plt.subplots()#figsize=[8,4])
    axes[0].axhline(0.,linestyle='--',color='grey')
    axes[0].scatter(df1['DATE'],df1['RCA_H'],
                color='k',
                linewidth=lw)
    axes[0].plot(df1['DATE'],df1['RCA_H'],
                color='k',
                linewidth=lw)
    axes[0].set_ylabel('RCA value')
    axes[0].set_title('Daily RCA values ($Z_H$) at '+locationstr+'\n PPI \n Clutter map and Baseline: 2018-03-13')
    axes[0].set_ylim(-5,25)
    axes[0].scatter(baseline1,0.0,marker='D',linewidth=lww,color='b')
    axes[0].text(xtext0,15,h_text1,size=size,family=family)
    axes[0].text(0.03, 0.87, '('+string.ascii_lowercase[0]+')', transform=axes[0].transAxes, 
            size=20, weight='regular')
    locs1, labs1 = plt.xticks()
    plt.xticks(locs1[::3])
    plt.xticks
    plt.gcf().autofmt_xdate()

    axes[1].axhline(0.,linestyle='--',color='grey')
    axes[1].scatter(df2['DATE'],df2['RCA_H'],
                color='k',
                linewidth=lw)
    axes[1].plot(df2['DATE'],df2['RCA_H'],
                color='k',
                linewidth=lw)
    axes[1].set_ylabel('RCA value')
    axes[1].set_title('Clutter map: composite      Baseline: 2018-01-25')
    axes[1].set_ylim(ylim)
    axes[1].scatter(baseline2,0.0,marker='D',linewidth=lww,color='b')
    axes[1].text(xtext0,ytext,h_text2,size=size,family=family)
    axes[1].text(0.03, 0.87, '('+string.ascii_lowercase[1]+')', transform=axes[1].transAxes, 
            size=20, weight='regular')
    locs2, labs2 = plt.xticks()
    plt.xticks(locs2[::3])
    plt.xticks
    plt.gcf().autofmt_xdate()
    plt.savefig(fig_outpath+'rca_h_ppi_'+site+inst+'_0313_composite.png')

    # # Plot the V polarization RCA values only
    # fig, ax = plt.subplots()#figsize=[8,4])
    # ax.axhline(0.,linestyle='--',color='grey')
    # ax.scatter(df['DATE'],df['RCA_V'],
    #             color='k',
    #             linewidth=lw)
    # ax.plot(df['DATE'],df['RCA_V'],
    #             color='k',
    #             linewidth=lw)
    # ax.set_ylabel('RCA value')
    # ax.set_title('Daily RCA values (V) at '+location+'\n PPI')
    # ax.set_ylim(ylim)
    # ax.scatter(baseline,0.0,marker='D',linewidth=lww,color='b')
    # ax.text(xtext0,ytext,v_text,size=size,family=family)
    # locs, labs = plt.xticks()
    # plt.xticks(locs[::7])
    # plt.xticks
    # plt.gcf().autofmt_xdate()
    # plt.savefig(fig_outpath+'rca_v_ppi_'+site+inst+'.png')

    # # Plot the H and V polarization RCA values together
    # fig, ax = plt.subplots()#figsize=[8,4])
    # ax.axhline(0.,linestyle='--',color='grey')
    # ax.scatter(df['DATE'],df['RCA_H'],
    #             color='k',
    #             linewidth=lw,
    #             label='H')
    # ax.plot(df['DATE'],df['RCA_H'],
    #             color='k',
    #             linewidth=lw,
    #             label='')
    # ax.scatter(df['DATE'],df['RCA_V'],
    #             color='slategrey',
    #             linewidth=lw,
    #             label='V')
    # ax.plot(df['DATE'],df['RCA_V'],
    #             color='slategrey',
    #             linewidth=lw,
    #             label='')
    # ax.legend()
    # ax.set_ylabel('RCA value')
    # ax.set_title('Daily RCA values at '+location+'\n PPI')
    # ax.set_ylim(ylim)
    # ax.grid(which='major',axis='both')
    # ax.scatter(baseline,0.0,marker='D',linewidth=lww,color='b')
    # ax.text(xtext0,ytext,h,size=size,family=family)
    # ax.text(xtext,ytext,v,size=size,family=family)
    # locs, labs = plt.xticks() 
    # plt.xticks(locs[::7]) 
    # plt.xticks
    # plt.gcf().autofmt_xdate()
    # plt.savefig(fig_outpath+'rca_hv_ppi_'+site+inst+'.png')
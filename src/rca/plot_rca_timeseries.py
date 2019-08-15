# plot_rca_timeseries.py

# generic RCA time series plotting

# combine all the random plotting scripts

# design it to be BASIC PLOTTING

# everyone can figure out how to plot CSV data how they want....

# Single radar
# H and V dual plot option

# Two radars

# Three radars

# Read in a .json file? have them specify site, inst, location??
site = ''
inst = ''
location = ''

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import string

def plot_rca_timeseries_oneradar(rca_file,output_directory,baseline_date,polarization,scan_type):
    """
    plot_rca_timeseries

     Parameters:
     --------------
     rca_file: str
             path to RCA CSV file
     output_directory: str
             path to directory for output .png file(s)
     baseline_date: str
             YYYY-MM-DD format of baseline date in this dataset
     polarization: str
             specify the polarization(s) desired
             'horizontal'
             'dual'
     scan_type: str
             specify if the map is for PPI or RHI
             'ppi'
             'rhi'
                       
     Returns:
     --------------
     (no specific return)
     however, plot is saved out

    """
    if scan_type == 'ppi':
        scan_type_label = 'PPI'
    elif scan_type == 'rhi':
        scan_type_label = 'RHI'
    
    ylim = -3.0,3.0
    lw = 1.0
    base_lw = 1.5
    ytext = 2.0
    xtext = 8.0
    xtext0 = 2.0

    params = {'mathtext.default': 'regular',
              'family': 'sans',
              'size': 11}          
    plt.rcParams.update(params)
    
    df = pd.read_csv(rca_file)
    df = df.sort_values(by='DATE')
    
    h_mean = str(np.nanmean(df['RCA_H']))[0:4] # slice only first 3 digits
    h_std = str(np.nanstd(df['RCA_H'],ddof=1))[0:4]
    h_min = str(min(df['RCA_H']))[0:4]
    h_max = str(max(df['RCA_H']))[0:4]
    h_text = ' \n Mean:  '+h_mean+' \n St. Dev.: '+h_std+' \n Min.:    '+h_min+' \n Max.:    '+h_max+''
        
    fig, ax = plt.subplots(figsize=[8,4])
    ax.axhline(0.,linestyle='--',color='grey')
    ax.scatter(df['DATE'],df['RCA_H'],
               color='k',
               linewidth=lw)
    ax.plot(df['DATE'],df['RCA_H'],
               color='k',
               linewidth=lw)
    ax.scatter(baseline_date,0.0,marker='D',linewidth=base_lw,color='b')
    ax.set_ylabel('RCA value (dB)')
    ax.set_title('Daily RCA values ($Z_H$) at '+location[0:3]+' '+location[3:]+' \n '+scan_type_label)
    ax.set_ylim(ylim)
    ax.text(xtext,ytext,h_text)
    locs, labs = plt.xticks()
    plt.xticks(locs[::1])
    plt.xticks
    plt.gcf().autofmt_xdate()
    plt.savefig(output_directory+'rca_h_'+scan_type+'_'+site+inst+'.png')
        
    if polarization == 'dual':
        v_mean = str(np.nanmean(df['RCA_V']))[0:4] # slice only first 3 digits
        v_std = str(np.nanstd(df['RCA_V'],ddof=1))[0:4]
        v_min = str(min(df['RCA_V']))[0:4]
        v_max = str(max(df['RCA_V']))[0:4]
        v_text = ' \n Mean:  '+v_mean+' \n St. Dev.:'+v_std+' \n Min.:   '+v_min+' \n Max.:   '+v_max+''
    
        fig, ax = plt.subplots(figsize=[8,4])
        ax.axhline(0.,linestyle='--',color='grey')
        ax.scatter(df['DATE'],df['RCA_V'],
                   color='k',
                   linewidth=lw)
        ax.plot(df['DATE'],df['RCA_V'],
                   color='k',
                   linewidth=lw)
        ax.scatter(baseline_date,0.0,marker='D',linewidth=base_lw,color='b')
        ax.set_ylabel('RCA value (dB)')
        ax.set_title('Daily RCA values ($Z_V$) at '+location[0:3]+' '+location[3:]+' \n '+scan_type_label)
        ax.set_ylim(ylim)
        ax.text(xtext,ytext,v_text)
        locs, labs = plt.xticks()
        plt.xticks(locs[::1])
        plt.xticks
        plt.gcf().autofmt_xdate()
        plt.savefig(output_directory+'rca_v_'+scan_type+'_'+site+inst+'.png')
        
        # Plot H and V together (one plot or dual plot?)
        fig, axes = plt.subplots(nrows=2,ncols=1,sharex=True,
                            figsize=[8,5])
        axes[0].axhline(0.,linestyle='--',color='grey')
        axes[0].scatter(df['DATE'],df['RCA_H'],
                    color='k',
                    linewidth=lw)
        axes[0].plot(df['DATE'],df['RCA_H'],
                    color='k',
                    linewidth=lw)
        axes[0].set_ylabel('RCA value (dB)')
        axes[0].set_title('Daily RCA values ($Z_H$) at '+location[0:3]+' '+location[3:]+'\n '+scan_type_label+' \n Clutter map and Baseline: 2018-03-13')
        axes[0].set_ylim(ylim)
        axes[0].scatter(baseline_date,0.0,marker='D',linewidth=base_lw,color='b')
        axes[0].text(xtext,ytext,h_text)
        axes[0].text(0.03, 0.87, '('+string.ascii_lowercase[0]+')', transform=axes[0].transAxes, 
                size=20, weight='regular')
        locs, labs = plt.xticks()
        plt.xticks(locs[::1])
        plt.xticks
        plt.gcf().autofmt_xdate()

        axes[1].axhline(0.,linestyle='--',color='grey')
        axes[1].scatter(df['DATE'],df['RCA_V'],
                    color='k',
                    linewidth=lw)
        axes[1].plot(df['DATE'],df['RCA_V'],
                    color='k',
                    linewidth=lw)
        axes[1].set_ylabel('RCA value (dB)')
        axes[1].set_title('Daily RCA values ($Z_V$) at '+location[0:3]+' '+location[3:]+'\n '+scan_type_label+'')
        axes[1].set_ylim(ylim)
        axes[1].scatter(baseline_date,0.0,marker='D',linewidth=base_lw,color='b')
        axes[1].text(xtext,ytext-1,v_text)
        axes[1].text(0.03, 0.87, '('+string.ascii_lowercase[1]+')', transform=axes[1].transAxes, 
                size=20, weight='regular')
        locs, labs = plt.xticks()
        plt.xticks(locs[::1])
        plt.xticks
        plt.gcf().autofmt_xdate()
        plt.savefig(output_directory+'rca_hv_'+scan_type+'_'+site+inst+'.png')

    
def plot_rca_timeseries_tworadar():
    
def plot_rca_timeseries_threeradar():

    
    

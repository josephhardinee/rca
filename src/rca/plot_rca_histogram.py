#!/usr/bin/env python
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import string

# Plot histogram of RCA values of CSAPR2 PPI derived and HSRHI derived

plt.style.use('publication')
params = {'mathtext.default': 'regular' }          
plt.rcParams.update(params)

directory = '/Users/hunz743/projects/taranis/taranis/calibration/'

csvfile = [directory+'daily_rcavalues_ppi_corcsapr2.csv',directory+'daily_rcavalues_hsrhi_corcsapr2_after1108.csv']
typ = ['ppi','hsrhi']
typ_label = ['PPI','RHI']
i = [0,1]

fig, ax = plt.subplots(nrows=2,ncols=1,figsize=[6,8],sharex=True,sharey=True)#figsize=[8,4])

for idx, x in enumerate(csvfile):

    df = pd.read_csv(x)
    # Ensure values in csv file are in chronological order
    df = df.sort_values(by='DATE')

    ax[0].set_title('Histogram of daily mean RCA values COR CSAPR2  \n 8 November 2018 - 19 December 2018 \n PPI')
    ax[1].set_title('RHI')
    #ax[i[idx]].set_title(typ_label[idx])
    ax[1].set_xlabel('RCA value')
    ax[i[idx]].set_ylabel('Count')
    ax[i[idx]].text(0.03, 0.87, '('+string.ascii_lowercase[idx]+')', transform=ax[i[idx]].transAxes, 
            size=20, weight='regular')

    #locs, labs = plt.xticks()

    ax[i[idx]].set_xlim(-1.0,1.0)

    ax[i[idx]].hist(df['RCA_H'])

plt.savefig(directory+'rca_hist_csapr2_ppirhi.png')


# SACR
csvfile = [directory+'daily_rcavalues_hsrhi_corxsacr_after1108.csv',directory+'daily_rcavalues_hsrhi_corkasacr_after1108.csv']
typ = ['ppi','hsrhi']
typ_label = ['PPI','RHI']
i = [0,1]

fig, ax = plt.subplots(nrows=2,ncols=1,figsize=[6,8],sharex=True,sharey=True)#figsize=[8,4])

for idx, x in enumerate(csvfile):

    df = pd.read_csv(x)
    # Ensure values in csv file are in chronological order
    df = df.sort_values(by='DATE')

    ax[0].set_title('Histogram of daily mean RCA values COR SACR  \n 8 November 2018 - 19 December 2018 \n XSACR')
    ax[1].set_title('KASACR')
    #ax[i[idx]].set_title(typ_label[idx])
    ax[1].set_xlabel('RCA value')
    ax[i[idx]].set_ylabel('Count')
    ax[i[idx]].text(0.03, 0.87, '('+string.ascii_lowercase[idx]+')', transform=ax[i[idx]].transAxes, 
            size=20, weight='regular')

    #locs, labs = plt.xticks()

    ax[i[idx]].set_xlim(-2.0,7.0)

    ax[i[idx]].hist(df['RCA_H'])

plt.savefig(directory+'rca_hist_sacr_rhi.png')
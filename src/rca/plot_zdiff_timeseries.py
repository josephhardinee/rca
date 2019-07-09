#!/usr/bin/env python
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.style.use('publication')
params = {'mathtext.default': 'regular' }          
plt.rcParams.update(params)
plt.rcParams["axes.grid"] = False

csvpath = './cross_compare/'
fig_outpath = './figures/'
csvfile1 = csvpath+'crosscal_cacti_xsacr_csapr2.csv'
csvfile2 = csvpath+'crosscal_cacti_xsacr_kasacr.csv'

# Change text box locations as needed
ylim = -10.0,20.0
lw = 0.3
lww = 0.3
#size = 11
#family = 'sans'

df = pd.read_csv(csvfile1)
#df['DateTime'] = df['DATE'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
# Ensure values in csv file are in chronological order
df = df.sort_values(by='DATE')
df2 = pd.read_csv(csvfile2)
#df2['DateTime'] = df2['DATE'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
# Ensure values in csv file are in chronological order
df2 = df2.sort_values(by='DATE')
#print(df['DateTime'])

fig, ax = plt.subplots()
ax.axhline(0.,linestyle='--',color='grey',zorder=-25)
ax.axhspan(-1.0, 1.0, facecolor='dimgrey', alpha=0.5,zorder=-100)
ax.axhspan(-2.0, 2.0, facecolor='gainsboro', alpha=0.5,zorder=-50)
ax.scatter(df['DATE'],df['ZDIFF_MED'],
           color='k',
           linewidth=lw,
           label='X - C')
ax.plot(df['DATE'],df['ZDIFF_MED'],
           color='k',
           linewidth=lww,
           label='')
ax.scatter(df2['DATE'],df2['ZDIFF_MED'],
           color='r',
           linewidth=lw,
           label='X - Ka')
ax.plot(df2['DATE'],df2['ZDIFF_MED'],
           color='r',
           linewidth=lww,
           label='')
ax.set_ylabel('dB')
ax.set_title('Daily median reflectivity (Z$_H$) difference at COR \n XSACR, CSAPR2, KaSACR')
ax.set_ylim(ylim)
ax.set_xlim('2018-11-08','2019-03-18')
ax.legend()
#ax.scatter(baseline,0.0,marker='D',linewidth=lww,color='b')
#ax.text(xtext0,ytext,h_text,size=size,family=family)
locs, labs = plt.xticks()
plt.xticks(locs[::14])
plt.xticks
#plt.xticks(labs[::1])
#plt.xticks
plt.gcf().autofmt_xdate()
plt.savefig(fig_outpath+'zdiff_cor.png')
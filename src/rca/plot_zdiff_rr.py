#!/usr/bin/env python
import numpy as numpy
import pandas as pd 
import matplotlib.pyplot as plt 

inst1 = 'xsacr'
inst2 = 'kasacr'
date = '20181111'
csvpath = '/Users/hunz743/'
csvfile = csvpath+'crosscompare_'+inst1+'_'+inst2+'_'+date+'.csv'
pluvio = csvpath+'Downloads/corwbpluvio2M1.a1.20181111.000000.custom.csv'

df = pd.read_csv(csvfile)
df = df.sort_values(by='TIME')

p = pd.read_csv(pluvio)
#p = p.sort_values(by='time_offset')


plt.plot(df['TIME'],df['ZDIFF_MEDIAN'])
plt.ylabel('Median Z(X) - Z(Ka)')
#plt.plot(p['intensity_rtnrt'][1:])
plt.savefig('/Users/hunz743/time_20181111.png')

plt.plot(p['time_offset'][1:],p['intensity_rtnrt'][1:])
plt.ylabel('Rain Rate')
plt.savefig('/Users/hunz743/rain_20181111.png')
#plt.show()




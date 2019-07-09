#!/usr/bin/env python
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib  import cm
import pandas as pd

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print(
            "ERROR: Arguments are csv file path, output path for figures, instrument1, instrument2, date"
        )
        sys.exit(0)

    csvpath = sys.argv[1]
    fig_outpath = sys.argv[2]
    inst1 = sys.argv[3]
    inst2 = sys.argv[4]
    date = sys.argv[5]
    print(csvpath, fig_outpath, inst1, inst2, date)

date = '20181127' 

#plt.style.use('publication')
csvfile = csvpath+'crosscompare_'+inst1+'_'+inst2+'_'+date+'.csv'

df = pd.read_csv(csvfile)
df = df.sort_values(by='TIME')
#time = df['TIME'][12:14]+df['TIME'][15:17]+df['TIME'][18:20]
time = np.arange(0,len(df['TIME']),1)
#print(time)

numps = df['NUM_PTS']
zdiffmed = df['ZDIFF_MEDIAN']
#if numps > 10000:
median = np.nanmedian(zdiffmed[numps>10000])
print(median)
print(numps[numps>10000])
#times = df['TIME']
#print(times[np.logical_and(numps>40000,numps<80000)])
#print(zdiffmed[np.logical_and(numps>40000,numps<80000)])
#time = time.dt.total_seconds()

plt.figure()
plt.hist(df['NUM_PTS'], bins = 10 ** np.linspace(np.log10(100), np.log10(20000), 50))
plt.gca().set_xscale('log')
#plt.hist(df['NUM_PTS'],bins=20,range=(0,3))
plt.xlabel('Number of points thru filter')
plt.ylabel('Count')
plt.title('Distribution of number of points that pass thru filtering \n '+date)
plt.savefig(fig_outpath+'numps_hist_'+date+'.png')

plt.figure()
plt.hist(df['ZDIFF_MEDIAN'],bins=10)
plt.xlabel('Median Z(X) - Z(Ka)')
plt.ylabel('Count')
plt.title('Distribution of median Z difference between '+inst1+' & '+inst2+' \n '+date)
plt.savefig(fig_outpath+'zdiff_hist_'+date+'.png')

fig = plt.figure()
ax = plt.gca()
#ax.scatter(data['o_value'] ,data['time_diff_day'] , c='blue', alpha=0.05, edgecolors='none')
ax.set_xscale('log')
#plt.figure()
scat = ax.scatter(df['NUM_PTS'],df['ZDIFF_MEDIAN'],c=time,cmap=cm.jet)
plt.colorbar(scat)#,ticks=df['TIME'])
plt.xlim(1,175000)
plt.ylabel('Median Z(X) - Z(Ka)')
plt.xlabel('Number of points thru filter')
plt.title(inst1+' & '+inst2+' \n '+date)
plt.savefig(fig_outpath+'zdiff_numps_'+date+'.png')

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
day = ['27']
month = '11'
year = '2018'

all_numps = []
all_zdiff = []

for idxd, d in enumerate(day):
    csvfile = csvpath+'crosscompare_'+inst1+'_'+inst2+'_'+year+month+d+'.csv'
    df = pd.read_csv(csvfile)
    all_numps.append(df['NUM_PTS'])
    all_zdiff.append(df['ZDIFF_MEDIAN'])

median = np.nanmedian(all_zdiff)

plt.figure()
plt.hist(all_zdiff,bins=15)
plt.xlabel('Median Z(X) - Z(Ka)')
plt.ylabel('Count')
plt.title('Distribution of median Z difference between '+inst1+' & '+inst2+' \n '+date)
plt.savefig(fig_outpath+'zdiff_hist_'+date+'.png')
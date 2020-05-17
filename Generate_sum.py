import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


os.chdir('/Users/ruairi/Google Drive/Code/Python/time tracker/Outputs')
def find_csv_filenames(suffix=".csv" ):
    filenames = os.listdir()
    return [ filename for filename in filenames if filename.endswith( suffix ) ]


filenames = find_csv_filenames()
for name in filenames:
    dat = pd.read_csv(name)
    date_of_data = dat.Date.iloc[0]

    dat['Start'] = pd.to_datetime(dat['Start'])
    dat['t-1'] = dat['Start'].shift(1)
    dat =dat[dat['t-1'].notnull()]

    dat['Time_on'] = dat['Start'] - dat['t-1']
    totals = pd.DataFrame(dat.groupby('Location')['Time_on'].sum())
    totals = totals.sort_values(by=['Time_on'] , ascending = False)
    totals['Time_on'] = totals['Time_on']/ np.timedelta64(1, 'm')

    # gen plot
    x= totals.index
    y= totals.Time_on
    plt.bar(x,y, color = 'green')
    plt.ylabel('Minutes')
    plt.xticks(rotation=45)
    path = str('plot_' +dat.Date.iloc[0] +'.png')
    plt.savefig(path)

    # Generate report
    al=totals.sum()
    report = str('Hi, this a is a report for: ' + date_of_data +
    '. Your total computer time was: ' + str(al.iloc[0].round(2)) + ' Minutes. ' +
    ' You spent the most time on: ' + str(totals.index[0]) + ' and you spent a total of '
    + str(totals.Time_on[0].round(2)) + ' Minutes there. ')
    path = str('report_' +dat.Date.iloc[0] +'.txt')
    text_file = open(path, "w")
    text_file.write(report)
    text_file.close()

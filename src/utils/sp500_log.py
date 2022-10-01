import pandas as pd
import yfinance
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
from matplotlib.ticker import ScalarFormatter
from math import log10
from scipy.signal import argrelextrema
from scipy.signal import find_peaks

def plot_lower_bound_index(index = "^GSPC"):
    # read S&P 500 data from 2000
    df = yfinance.download('^GSPC', start='1910-01-01', end='2022-09-30', interval="1mo")
    fig, ax = plt.subplots()
    ax.plot(df.index, df['Adj Close'], color='black')
    ax.set_yscale("log")
    # ax.yaxis.set_major_formatter(ScalarFormatter())
    # ax.minorticks_off()

    # have weekly plot, but just grab a data point every month to compute the argrelextrema, but in that case need to search by date.

    # get all local min and max using argrelextrema
    local_min = argrelextrema(df['Adj Close'].values, np.less, 0, 5)[0]
    local_max = argrelextrema(df['Adj Close'].values, np.greater,0, 5)[0]

    # plot all local min and max
    ax.plot(df.index[local_min], df['Adj Close'][local_min], 'o', color='red')
    ax.plot(df.index[local_max], df['Adj Close'][local_max], 'o', color='green')
    # save plot

    new_df = df

    # draw line through local_min
    new_df.reset_index(inplace=True)
    new_df['Date'] = new_df['Date'].apply(mpl_dates.date2num)
    new_df = new_df.astype(float)

    # grab last point in local_min and 2nd to first point in local_min
    # and draw a line between them
    last_min_point = new_df.iloc[local_min[-1]]
    first_min_point = new_df.iloc[local_min[0]]
    # draw line between last_min_point and first_min_point
    # y = mx + b
    m = (last_min_point['Adj Close'] - first_min_point['Adj Close']) / (last_min_point['Date'] - first_min_point['Date'])
    b = last_min_point['Adj Close'] - m * last_min_point['Date']
    # ax.set_yscale("linear")
    ax2 = ax.twinx()
    ax2.set_yscale("linear")
    custom_ylim = (0, 7000)
    plt.setp(ax2, ylim=custom_ylim)


    # mx+b for local_max
    last_min_point = new_df.iloc[local_min[-1]]
    first_min_point = new_df.iloc[local_min[8]]
    # draw line between last_min_point and first_min_point
    # y = mx + b
    m = (last_min_point['Adj Close'] - first_min_point['Adj Close']) / (last_min_point['Date'] - first_min_point['Date'])
    b = last_min_point['Adj Close'] - m * last_min_point['Date']
    # ax2.set_ylabel('Other line', color='b')
    # ax2.plot(new_df['Date'], slope * (new_df['Date']) + intercept, color='blue')

    # draw slope
    ax2.plot(new_df['Date'], m * new_df["Date"] + b, color='green')


    last_max_point = new_df.iloc[local_max[-2]]
    first_max_point = new_df.iloc[local_max[1]]
    # draw line between last_max_point and first_max_point
    # y = mx + b
    m = (last_max_point['Adj Close'] - first_max_point['Adj Close']) / (last_max_point['Date'] - first_max_point['Date'])
    b = last_max_point['Adj Close'] - m * last_max_point['Date']
    # convert this to a percent of the max ylim
    ax2.plot(new_df['Date'], m * new_df["Date"] + b+3500, color='red')
    # best_fit = np.polyfit(np.log(new_df["Date"][local_min]), np.log10(new_df['Adj Close'][local_min]), 1)
    # draw lines through local_min points
    # best_fit = np.polyfit(np.log(df.index[local_min]), np.log(df['Adj Close'][local_min]), 1)
    # plot best_fit line
    # print(best_fit)

    # best_Fit_series = best_fit[0] * new_df["Date"] + best_fit[1]
    # log 10 entire line
    # best_Fit_series = np.log10(best_Fit_series)
    # ax.plot(new_df["Date"], best_fit[0] * new_df["Date"] + best_fit[1], color='black')


    # plot line going through local_min
    # plot line going through local_max
    fig.savefig('sp500_log.png', dpi=300, bbox_inches='tight')
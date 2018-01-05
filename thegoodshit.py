import csv
import math
import random as rd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime as dt


now = dt.datetime.now().timestamp()
rd.seed(now)


#constants
SET_SIZE = 100
PLOT_WIDTH = 100


def get_stock(ticker, max_size, offset):
    points = np.empty([max_size, 2])
    data = open('/Users/julio/data/STOCKS/' + ticker + '.csv')
    reader = csv.DictReader(data)
    for i in range(offset):
        reader.__next__()
    i = 0
    for row in reader:
        time = dt.datetime.strptime(row['Date'], '%Y-%m-%d').timestamp()
        price   = row['AdjClose']
        points[i] = np.array([time, price])
        i += 1
        if (i >= max_size):
            break
    points = np.flip(points, 0)
    return points

def unix_to_date(ts):
    return dt.datetime.fromtimestamp(ts)
unix_to_date = np.vectorize(unix_to_date)
cat_stocks = get_stock('AAPL', SET_SIZE, 0)

def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / N

fig, ax = plt.subplots()


# get x and y
# plot raw input as a marker
x, y = cat_stocks.T
x = unix_to_date(x)
ax.plot(x, y, label="raw")


# calculate running mean
n = 5
rm = running_mean(y, n)
#plot running_mean as a marker
ax.plot(x[n - 1:], rm, label="rm"+str(n))

#calculate gradient of running mean
dydx2 = np.gradient(rm)
ax.plot(x[n - 1:], dydx2, label="rm gradient")
ax.plot(x[n - 1:], np.where(dydx2 > 0, dydx2, 0), label="rm +gradient")
#ax.plot(x[n - 1:], np.where(dydx2 < 0, dydx2, 0), label="rm -gradient")
ax.plot(x[n - 1:], np.where(dydx2 < 0, -25, 25), label="rm binary")

#calculate the maximum profit
    # integral(max(0, dydx))
profit = np.cumsum(np.where(dydx2 > 0, dydx2, 0))
ax.plot(x[n - 1:], profit, label="maximum profit")

ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.xaxis.set_minor_locator(mdates.MonthLocator())


plt.legend()
plt.show()

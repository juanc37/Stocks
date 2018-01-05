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
SET_SIZE = 10000
SLIDE_LENGTH = 1
PLOT_WIDTH = 10


class stock:
    def __init__(self, ticker, max_size, offset):
        self.points = np.empty([max_size, 2])
        with open('/Users/julio/data/STOCKS/' + ticker + '.csv') as data:
            reader = csv.DictReader(data)
            for i in range(offset):
                reader.__next__()
            i = 0
            for row in reader:
                time = dt.datetime.strptime(row['Date'], '%Y-%m-%d').timestamp()
                price   = row['AdjClose']
                self.points[i] = np.array([time, price])
                i += 1
                if (i >= max_size):
                    self.points = np.flip(self.points, 0)
                    return
            self.points = np.flip(self.points[:i - max_size], 0)





def unix_to_date(ts):
    return dt.datetime.fromtimestamp(ts)
unix_to_date = np.vectorize(unix_to_date)

fig, ax = plt.subplots()

cat_stocks = stock('AAPL', 1000, 0)

# get x and y
x, y = cat_stocks.points.T
x = unix_to_date(x)
ax.plot(x, y, label="raw")

# calculate the gradient
dydx1 = np.gradient(y)
#ax.plot(x, dydx, label="gradient")


# calculate running mean
n = 50
def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / N
rm = running_mean(y, n)
ax.plot(x[n - 1:], rm, label="rm"+str(n))

#calculate gradient of running mean
dydx2 = np.gradient(rm)
ax.plot(x[n - 1:], dydx2, label="rm gradient")
ax.plot(x[n - 1:], np.where(dydx2 > 0, dydx2, 0), label="rm +gradient")
ax.plot(x[n - 1:], np.where(dydx2 < 0, dydx2, 0), label="rm -gradient")
#ax.plot(x[n - 1:], np.where(dydx2 < 0, -25, 25), label="rm binary")

profit = np.cumsum(np.where(dydx2 > 0, dydx2, 0))
ax.plot(x[n - 1:], profit, label="maximum profit")

ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.xaxis.set_minor_locator(mdates.MonthLocator())


plt.legend()
plt.show()

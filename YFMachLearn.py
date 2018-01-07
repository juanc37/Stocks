import csv
import sklearn.svm as SVR
import matplotlib.pyplot as plt
import numpy as np
class stock():
    date = ""
    open = 0
    high = 0
    low = 0
    close = 0
    volume = 0
    def __init__(self, date, open, high, low, close, volume):
        self.date = self.parseDate(date)
        self.open = open,
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
    def parseDate(self,date):
        newdate = date[:4]
        newdate += date[5:7]
        newdate += date[8:]
        return newdate

def predict_prices(dates, price, x):
    dates = np.reshape(dates,(len(dates),1))

    svr_lin = SVR.SVR(kernel = 'linear', C=1e3)
    # svr_poly = SVR.SVR(kernel = 'poly', C=1e3, degree = 2)
    svr_rbf = SVR.SVR(kernel = 'rbf', C=1e3, gamma = 0.1)
    svr_lin.fit(dates,price)
    # svr_poly.fit(dates,price)
    svr_rbf.fit(dates,price)
    plt.scatter(dates,price, color='black', label = 'Data')
    plt.plot(dates,svr_rbf.predict(dates), color = 'red', label='RBF model')
    plt.plot(dates, svr_lin.predict(dates), color='green', label='Linear Model')
    # plt.plot(dates, svr_poly.predict(dates), color='blue', label='Polynomial Model')
    plt.tick_params(direction='out', length=1, width=1, colors='r')
    plt.xlabel('days')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
    return  svr_lin.predict(x)[0], svr_rbf.predict(x)[0]#  svr_poly.predict(x)[0]

def parseCSV():
    prices = []
    with open('AAL.csv', newline='') as data:
        reader = csv.DictReader(data)
        for row in reader:
            prices.append(stock(row['Date'], row['Open'], row['High'], row['Low'], round(float(row['Close']),2), row['Volume']))
    return prices
stocks = parseCSV()
dates = [x.date for x in stocks[0:100]]
prices= [x.prices for x in stocks[0:100]]
for item in range(100):
    dates.append(item)
    prices.append(stocks[item+1500].close)
predict = predict_prices(dates,prices,100)
print (predict)



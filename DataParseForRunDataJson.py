import numpy as np
import sklearn.svm as SVR
import matplotlib.pyplot as plt
import json

class stockInstance():
    date = ""
    tradePrice = 0
    name = ""
    secondCount = 0
    def __init__(self,date,tradePrice,name):
        self.date = date[:-1]
        self.tradePrice = tradePrice
        self.name = name
        self.secondCount = self.getSecondCount()
    def getHour(self):
        return (int)(self.date[-8:-6])
    def getMinute(self):
        return (int)(self.date[-5:-3])
    def getSecond(self):
        return (int)(self.date[-2:])
    def getSecondCount(self):
        return (((self.getHour()*60)*60) + (self.getMinute() *60) + self.getSecond())


def createVectorForRun(filePath):
    run = []
    data = json.load(open(filePath))
    for item in data:
        run.append(stockInstance(item['updated_at'],item['last_trade_price'],item['symbol']))
    return run
def getPlotAxises(run):
    sec = []
    price = []
    firstSec = run[0].secondCount
    for item in run:
        sec.append(item.secondCount - firstSec)
        price.append(item.tradePrice)
    return sec, price


run = createVectorForRun('run7024.json')
def predict_prices(dates, price, x):
    dates = np.reshape(dates,(len(dates),1))

    svr_lin = SVR.SVR(kernel = 'linear', C=1e3)
    # svr_poly = SVR.SVR(kernel = 'poly', C=1e3, degree = 2)
    # svr_rbf = SVR.SVR(kernel = 'rbf', C=1e3, gamma = 0.1)
    svr_lin.fit(dates,price)
    # svr_poly.fit(dates,price)
    # svr_rbf.fir(dates,price)
    plt.scatter(dates,price, color='black', label = 'Data')
    # plt.plot(dates,svr_rbf.predict(dates), color = 'red', label='RBF model')
    plt.plot(dates, svr_lin.predict(dates), color='green', label='Linear Model')
    # plt.plot(dates, svr_poly.predict(dates), color='blue', label='Polynomial Model')
    plt.xlabel('Seconds')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
    return  svr_lin.predict(x)[0]#, svr_poly.predict(x)[0], svr_rbf.predict(x)[0],
dates, price = getPlotAxises(run)
predict = predict_prices(dates,price, 29)
print (predict)

# plt.title(run[0].name)
# plt.xlabel('Seconds')
# plt.ylabel('Price')
# plt.plot(dates, price, 'o', linestyle='-')
# plt.show()


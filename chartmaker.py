import numpy as np
import matplotlib.pyplot as plt
import csv

ID = "X1-ZWz1g40n2yi58r_adn99"
class zillow():
    state = ""
    month = 0
    year = 1996
    medianHomePrice = 0
    def __init__(self, state, month, year, medianHomePrice):
        self.state = state
        self.month = month
        self.year = year
        self.medianHomePrice = medianHomePrice
    def getprice(self):
        return self.medianHomePrice

def nextPeriod(year, month):
    if (month == 12):
        month = 0
        year += 1
    month += 1
    return year, month

def periodString(year, month):
    if (month < 10):
        return str(year) + "-0" + str(month)
    return str(year) + "-" + str(month)


def parseCSV():
    global prices, data, year, month
    prices = []
    with open('State_Zhvi_2bedroom.csv', newline='') as data:
        reader = csv.DictReader(data)
        for row in reader:
            count = 0
            year = 1996
            month = 4
            while (count != -1):
                prices.append(zillow(row['RegionName'], month, year, row[periodString(year, month)]))
                year, month = nextPeriod(year, month)
                if (year == 2017 and month == 9):
                    count = -1
    return prices


def getYearly(prices, state):
    months = []
    homeprice = []
    global data
    for data in prices:
        if (data.state == state and data.month == 1):
            months.append(data.year)
    for data in prices:
        if (data.state == state and data.month == 1):
            homeprice.append(data.medianHomePrice)
    return months, homeprice

def getMonthly(prices, state):
    monthCount = 0
    months = []
    homeprice = []
    for data in prices:
        if (data.state == state):
            months.append(monthCount)
            homeprice.append(data.medianHomePrice)
            monthCount+=1
    return months, homeprice


prices = parseCSV()
months, homeprice = getMonthly(prices, 'California')

plt.xlabel('Month (Starting at 1996)')
plt.ylabel('Price')
plt.plot(months, homeprice, 'o', linestyle='-')
plt.show()


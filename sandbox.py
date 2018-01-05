import csv
import datetime as dt
import matplotlib.pyplot as plt

date = []
price = []
with open('/Users/julio/data/STOCKS/AAPL.csv') as data:
        reader = csv.DictReader(data)
        for row in reader:
            date.append(dt.datetime.strptime(row['Date'], '%Y-%m-%d').timestamp())
            price.append(row['AdjClose'])



plt.plot(date, price)
plt.show()

import csv
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
        print (newdate)
        return newdate

def parseCSV():
    prices = []
    with open('AAL.csv', newline='') as data:
        reader = csv.DictReader(data)
        for row in reader:
            prices.append(stock(row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Volume']))

    return prices
stocks = parseCSV()



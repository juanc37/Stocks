import csv
import numpy as np

#TODO - add a tracker array

class Sim:
    def __init__(self, ticker, max_size, offset, bank_init):
        self._prices = np.empty(max_size)
        self._bank = int(bank_init)
        self._bank_init = int(bank_init)
        self._shares = int(0)
        self._now = 0
        self._i = -1
        self._tracker = []
        with open('/Users/julio/data/stocks1/' + ticker + '.csv') as data:
            reader = csv.DictReader(data)
            for i in range(offset):
                reader.__next__()
            i = 0
            for row in reader:
                self._prices[i] = float(row['AdjClose'])
                if (i >= max_size - 1):
                    break
                else:
                    i += 1
        self._prices = np.flip(self._prices[:i - max_size], 0)

    def __iter__(self):
        return self

    def __next__(self):
        self._i += 1
        if (self._i == len(self._prices)):
            raise StopIteration
        self._now = self._prices[self._i]
        self._tracker.append(self.get_profit())
        return self._now

    def get_bank(self):
        return self._bank

    def get_shares(self):
        return self._shares

    def sell(self, x):
        i = int(x)
        if (i > self._shares):
            return 0
        else:
            self._shares -= i
            self._bank += i * self._now
            return (i * self._now)
    def sell_all(self):
        self.sell(self._shares)

    def buy(self, x):
        i = int(x)
        price = i * self._now
        if (price > self._bank):
            return 0
        else:
            self._bank -= price
            self._shares += i
            return price

    def buy_all(self):
        max_stocks = self._bank / self._now
        self.buy(int(max_stocks))

    def get_assets(self):
        return self._bank + (self._shares * self._now)

    def get_profit(self):
        assets = self._bank + (self._shares * self._now)
        return assets - self._bank_init
    def get_track(self):
        return self._tracker

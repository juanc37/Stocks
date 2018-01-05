import pymysql.cursors
import numpy as np
import dateutil.parser as dtp
import datetime as dt

#TODO - add a tracker array

class Sim:
    def __init__(self, ticker, bank_init, iters):
        self._bank = int(bank_init)
        self._bank_init = int(bank_init)
        self._shares = int(0)

        self._max = iters
        self._i = 0

        self._prices = []
        self._asset_track = []
        self._own_track = []

        self._con = pymysql.connect(host='localhost', user='root', db='stocks')
        self._cursor = self._con.cursor()
        self._sql = 'SELECT AVG(bid_price) FROM moment WHERE time_stamp BETWEEN TIMESTAMP(\'{time}\') AND DATE_ADD(TIMESTAMP(\'{time}\') , INTERVAL 7 SECOND);'

        self._cursor.execute('SELECT time_stamp FROM moment ORDER BY time_stamp ASC LIMIT 1;')
        self._time = self._cursor.fetchone()[0]

        self._now = self._cursor.execute(self._sql.format(time=self._time.isoformat(' ')))

    def __iter__(self):
        return self

    def __next__(self):
        self._i = self._i + 1
        if self._i > self._max:
            raise StopIteration

        self._time = self._time + dt.timedelta(seconds=7)
        self._cursor.execute(self._sql.format(time=self._time.isoformat(' ')))
        res = self._cursor.fetchone()[0]

        if res == None:
            res = self._now
            print(self._time)

        self._now = res

        self._prices.append(self._now)
        self._asset_track.append(self.get_profit())
        self._own_track.append(self.get_shares())
        #print(self._now)
        return self._now

    def get_bank(self):
        return self._bank

    def get_shares(self):
        return self._shares

    def sell(self, x):
        i = int(x)
        if i > self._shares:
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
        if price > self._bank:
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

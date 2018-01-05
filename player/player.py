"""
This script will pull stock data and send orders to the simulation methods

it contains a main loop which does the following things in order:
1. Pull stock data
2. Make decision
3. Log the activity of the loop
"""
import sys
sys.path.append('/Users/julio/lib/python/stocks')

import json
import numpy as np
import matplotlib.pyplot as plt
from simulation.simulator_csv import Sim


sim = Sim('AAPL', 500, 1500)

#slider
class Runner:
    def __init__(self, run_lenght):
        self._run_length = run_lenght
        self.values = np.zeros(run_lenght * 2)

    def insert(self, val):
        self.values = np.roll(self.values, 1)
        self.values[0] = val

    def avg(self):
        run = self.values[:self._run_length]
        return run.mean()

    def delta(self):
        run1 = self.values[:self._run_length]
        run2 = self.values[self._run_length:]
        return run1.mean() - run2.mean()

async def log(*string):
    #with open('stocks.log') as data:
    #    data.write(string)
    print(string)

rnr = Runner(1)

run_delta_track = []
run_price_track = []

i = 0
for itr in sim:
    rnr.insert(itr)

    i = i + 1
    if i < 4:
        run_delta_track.append(0)
        run_price_track.append(156)
        continue

    run_delta_track.append(rnr.delta())
    run_price_track.append(rnr.avg())
    if rnr.delta() < 0.01:
        sim.sell_all()
    else:
        sim.buy_all()

plt.plot(run_delta_track, label='run gradient')
plt.plot(np.array(run_price_track) - 157, label='run price')
plt.plot(np.gradient(sim._prices), label='gradient')
plt.plot(np.array(sim._prices) - 157, label='prices')
plt.plot(sim._asset_track, label='assets')
plt.plot(np.array(sim._own_track) / 10, label='shares')
plt.legend()
plt.show()
print('profit', sim.get_profit())

# def calculate(price):
#
#
#
# def main_loop():
#     #

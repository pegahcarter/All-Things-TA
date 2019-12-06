import pandas as pd
import numpy as np
from datetime import datetime

class Portfolio:

    x_leverage = 10
    trade_size = .1
    profit_levels = [.5, 1, 2, 3]
    initial_capital = 10000

    def __init__(self, tp_pcts):
        self.available_capital = self.initial_capital
        self.positions = []
        self.tp_pcts =  tp_pcts
        self.index_tp_hit_set = set()
        self.index_closed_set = set()

    def positions_open(self):
        return len(self.positions)

    def open_position(self, position):
        d_amt = self.available_capital * self.trade_size
        self.available_capital -= d_amt
        position['d_amt'] = d_amt * self.x_leverage

        self.index_tp_hit_set.update(position['index_tp_hit'])
        self.index_closed_set.add(position['index_closed'])
        self.positions.append(position)

    def sell_position(self, hr, position):
        pos = position['index_tp_hit'].index(hr)
        profit_level = self.profit_levels[pos]
        pct_sold = self.tp_pcts[pos + 1]

        base_sold = position['d_amt'] * pct_sold/100
        profit = base_sold * position['pct_open'] * position['pct'] * profit_level / 100

        base_sold /= self.x_leverage

        position['pct_open'] -= pct_sold
        position['index_tp_hit'][pos] = None

        self.available_capital += base_sold + profit


    def close_position(self, position):

        self.positions.pop(self.positions.index(position))
        pct_sold = position['pct_open']

        base_sold = position['d_amt'] * pct_sold/100
        if position['tp'] == 4:
            return
        elif position['tp'] == 0:
            profit = -base_sold * position['pct']
        else:
            profit = 0

        base_sold /= self.x_leverage

        self.available_capital += base_sold + profit
        if 'USDT' in position['ticker']:
            self.available_capital -= position['d_amt'] * .0005
        else:
            self.available_capital -= position['d_amt'] * .002

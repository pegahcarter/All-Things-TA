import pandas as pd
import numpy as np
from datetime import datetime

class Portfolio:

    initial_capital = 10000
    x_leverage = 1
    trade_size = .1

    def __init__(self, *args, **kwargs):
        self.available_capital = self.initial_capital
        self.positions = []

    def positions_open(self):
        return len(self.positions)

    def open_position(self, pct_capital, **position):
        self.num_positions += 1
        position['d_amt'] = self.available_capital * pct_capital
        self.available_capital -= position['d_amt']
        self.positions.append(
            position
        )

    def close_position(self, x_leverage, **position):
        self.available_capital += position['d_amt'] * (1 + position['net_profit'] * x_leverage)
        return self.positions.pop(self.positions.index(position))

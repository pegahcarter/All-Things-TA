import pandas as pd
import numpy as np
from datetime import datetime

class Portfolio:

    def __init__(self, *args, **kwargs):
        self.PORTFOLIO_START_VALUE = 10000.
        self.available_capital = self.PORTFOLIO_START_VALUE
        self.num_positions = 0
        self.positions = []


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

import pandas as pd
import numpy as np
from datetime import datetime

class Portfolio:

    def __init__(self, *args, **kwargs):
        self.PORTFOLIO_START_VALUE = 10000.
        self.available_capital = self.PORTFOLIO_START_VALUE
        self.num_positions = 0
        self.positions = []


    def open_position(self, **kwargs):
        self.num_positions += 1
        kwargs['d_amt'] = self.available_capital * .01
        self.available_capital -= kwargs['d_amt']
        self.positions.append(
            kwargs
        )


    def close_position(self, position):
        self.available_capital += position['d_amt']*(position['net_profit']*10) + position['d_amt']
        # return self.positions.pop(self.positions.index(position))

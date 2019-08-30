import pandas as pd
import numpy as np
from datetime import datetime

class Portfolio:

    def __init__(self, *args, **kwargs):
        self.PORTFOLIO_START_VALUE = 10000.
        self.available_capital = self.PORTFOLIO_START_VALUE
        self.num_positions = 0
        # self.positions = {ticker: [] for ticker in tickers}
        self.positions = {'BTC/USD': []}


    def open_position(self, ticker, **kwargs):
        self.num_positions += 1
        kwargs['d_amt'] = self.available_capital * .25
        self.available_capital -= kwargs['d_amt']
        self.positions[ticker].append(
            kwargs
        )


    def close_position(self, ticker, position):
        self.available_capital += position['d_amt']*(position['net_profit'])*10 + position['d_amt']
        return self.positions[ticker].pop(self.positions[ticker].index(position))

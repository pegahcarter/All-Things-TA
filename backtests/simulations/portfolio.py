import pandas as pd
import numpy as np
from datetime import datetime

class Portfolio:

    def __init__(self, *args, **kwargs):
        self.PORTFOLIO_START_VALUE = 10000
        self.available_capital = self.PORTFOLIO_START_VALUE
        self.num_positions_open = 0
        self.positions = {ticker: [] for ticker in tickers}



    def open_position(self, *args, **kwargs):
        pass


    def close_position(self, *args, **kwargs):
        pass

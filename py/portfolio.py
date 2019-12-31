import pandas as pd
import numpy as np
from datetime import datetime

class Portfolio:

    x_leverage = 10
    trade_size = .1
    # NOTE: rr = risk/return
    rr_list = [-1, .5, 1, 2, 3]
    initial_capital = 10000

    def __init__(self, tp_pcts):
        self.available_capital = self.initial_capital
        self.positions = []
        self.tp_pcts = tp_pcts


    def _add_fee(self, ticker, trade_value, side, profit=0):

        if ticker == 'ETH-USDT' or ticker == 'BTC-USDT':
            if side == 'buy':
                rate = .00075
            else:  # side == 'sell'
                rate = -.00025
        else:    # ticker is not a perpetual contract
            if side == 'buy':
                rate = .0025
            else:  # side == 'sell'
                rate = -.0005

        fee = (trade_value + profit) * rate
        self.available_capital -= fee


    def _trade(self, ticker, trade_value, profit=0, side='long', method='open'):

        base_value = trade_value / self.x_leverage
        if side == 'buy':
            self.available_capital -= base_value
        else:  # side == 'sell'
            self.available_capital += base_value + profit

        self._add_fee(ticker, trade_value, side, profit)


    def _manage_positions(self, position, method):

        if method == 'open':
            self.positions.append(position)
        elif method == 'close':
            position_index = self.positions.index(position)
            self.positions.pop(position_index)


    def open(self, position):

        trade_value = self.available_capital * self.trade_size * self.x_leverage
        position['dollar_value'] = trade_value
        self._trade(position['ticker'], trade_value, side=position['signal'], method='open')
        self._manage_positions(position, method='open')


    def sell(self, position, index_of_action=None):

        tp_index = position['index_tp_hit'].index(index_of_action)

        rr = self.rr_list[tp_index]
        pct_sold = self.tp_pcts[tp_index]

        trade_value = position['dollar_value'] * pct_sold
        profit = rr * trade_value * position['pct_open'] * position['pct']

        position['index_tp_hit'][tp_index] = None
        position['pct_open'] -= pct_sold

        self._trade(position['ticker'], trade_value, profit=profit, side='sell')

        # Close position
        if tp_index == position['tp']:
            self._manage_positions(position, method='close')

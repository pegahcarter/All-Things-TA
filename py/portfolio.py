import pandas as pd
import numpy as np
from datetime import datetime

class Portfolio:

    x_leverage = 10
    trade_size = .1
    # NOTE: rr = risk/return
    rrs = [-1, .5, 1, 2, 3]
    initial_capital = 10

    def __init__(self, tp_pcts):
        self.available_capital = self.initial_capital
        self.fees = 0
        self.positions = []
        self.tp_pcts = tp_pcts
        self.tps = { tp: {'rr': rr, 'pct_sold': pct_sold} \
                     for tp, (pct_sold, rr) in enumerate(zip(tp_pcts, self.rrs))
                    }


    def _add_fee(self, ticker, trade_value, profit, signal, method):

        if ticker == 'ETH-USDT' or ticker == 'BTC-USDT':
            if (signal == 'long' and method == 'buy') or (signal == 'short' and method == 'sell'):
                rate = .00075
            else:  # (signal == 'long' and method == 'sell') or (signal == 'short' and method == 'buy'):
                rate = -.00025
        else:    # ticker is not a perpetual contract
            if (signal == 'long' and method == 'buy') or (signal == 'short' and method == 'sell'):
                rate = .0025
            else:  # (signal == 'long' and method == 'sell') or (signal == 'short' and method == 'buy'):
                rate = -.0005

        fee = (trade_value + profit) * rate
        self.available_capital -= fee
        self.fees += fee


    def _trade(self, ticker, trade_value, profit=0, signal='long', method='buy'):

        base_value = trade_value / self.x_leverage
        if method == 'buy':
            self.available_capital -= base_value
        else:  # method == 'sell'
            self.available_capital += base_value + profit

        self._add_fee(ticker, trade_value, profit, signal, method)


    def has_open_positions(self):
        return len(self.positions) > 0


    def open(self, position):

        trade_value = self.available_capital * self.trade_size * self.x_leverage
        position['dollar_value'] = trade_value
        position['pct_open'] = 1

        self._trade(position['ticker'], trade_value, signal=position['signal'], method='buy')
        self.positions.append(position)


    def sell(self, position, index_of_action=None):

        tp_index = position['index_tp_hit'].index(index_of_action)

        pct_sold = self.tps[tp_index]['pct_sold']
        rr = self.tps[tp_index]['rr']

        trade_value = position['dollar_value'] * pct_sold
        profit = rr * trade_value * position['pct_open'] * position['pct']

        position['index_tp_hit'][tp_index] = None
        position['pct_open'] -= pct_sold

        self._trade(position['ticker'], trade_value, profit=profit, signal=position['signal'], method='sell')


    def close(self, position):

        # Sell whatever remains of position
        if position['pct_open'] > 0:
            trade_value = position['dollar_value'] * position['pct_open']
            self._trade(position['ticker'], trade_value, signal=position['signal'], method='sell')

        # Close position
        pos_index = self.positions.index(position)
        self.positions.pop(pos_index)

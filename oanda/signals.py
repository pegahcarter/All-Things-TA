# Create signals
from base import base
from variables import trade_size_dict

import pandas as pd
import os


def signals(trade_min=0, trade_max=1, directory='../data/oanda/', tp=False, **kwargs):
    ''' Determines when to open trades'''
    _signals = []

    for csvfile in os.listdir(directory):
        ticker = csvfile[:csvfile.find('.')]
        df = pd.read_csv(directory + csvfile)

        # Add coin signals to primary signal list
        trade_size = trade_size_dict[ticker]
        coin_signals = base(df, ticker=ticker, **trade_size)
        if tp:
            determine_TP(df, coin_signals)
        _signals.extend(coin_signals)

    # Re-order signals by index opened
    _signals = sorted(_signals, key=lambda x: x['index_opened'])

    return _signals



def determine_TP(df, signals):
    ''' Figure out which TP level is hit '''

    low = df['low'].tolist()
    low_inverse = (-df['low']).tolist()
    high = df['high'].tolist()
    high_inverse = (-df['high']).tolist()

    for i, row in enumerate(signals):
        price = row['price']
        stop_loss = row['stop_loss']
        if row['signal'] == 'long':
            l_bounds = low
            u_bounds = high
        else:   # signal == 'short'
            l_bounds = high_inverse
            u_bounds = low_inverse
            price *= -1
            stop_loss *= -1

        diff = price - stop_loss

        tp1 = price + diff/2.
        tp2 = price + diff

        tp_targets = [tp1, tp2]
        index_tp_hit = [None, None, None]
        tp = 0

        for x in range(row['index_opened'] + 1, len(df)):
            if tp == 2 or l_bounds[x] < stop_loss:
                # Add index hit for stop loss
                if tp == 0:
                    index_tp_hit[0] = x
                break
            while tp != 2 and u_bounds[x] > tp_targets[tp]:
                tp += 1
                index_tp_hit[tp] = x
            if tp > 0:
                stop_loss = price

        # Remove signal if position never fully closes before end of price data
        # NOTE: Could this fuck up logic if we pop the second to last signal, but
        #   keep the last signal?  `i` could be referencing a non-existing index.
        if x == len(df):
            signals.pop(i)

        signals[i]['tp'] = int(tp)
        signals[i]['index_tp_hit'] = index_tp_hit
        signals[i]['index_closed'] = x

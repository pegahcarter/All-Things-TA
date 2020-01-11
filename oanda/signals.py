# Create signals
from base import base
import pandas as pd
import os


def signals(trade_min=0, trade_max=1, directory='../data/oanda/'):

    _signals = []

    for csvfile in os.listdir(directory):
        ticker = csvfile[:csvfile.find('.')]
        df = pd.read_csv(directory + csvfile)

        # Add coin signals to primary signal list
        coin_signals = base(df, ticker=ticker)
        _signals.extend(coin_signals)

    # Re-order signals by index opened
    _signals = sorted(_signals, key=lambda x: x['opened'])

    return _signals

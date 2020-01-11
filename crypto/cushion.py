# Analyzing effects of cushion trades
from functions import *
from portfolio import Portfolio
import itertools
import os
import ujson


tp_pcts = [1, .05, .95, 0, 0]

cushion_list = [round(0.0025 - 0.0001*x, 4) for x in range(50)]
results = pd.Series(index=cushion_list, name='available_capital')

for cushion in cushion_list:

    signals = []
    # Load signals
    for f in os.listdir('../data/binance/'):

        df = pd.read_csv('../data/binance/' + f)
        coin_signals = find_signals(df, window_fast=21, window_mid=30, window_slow=50, cushion=cushion)

        # Add `tp`, `index_tp_hit`, and `index_closed`
        determine_TP(df, coin_signals)

        # Add ticker to signal & remove unused keys
        ticker = f[:f.find('.')]
        for x in coin_signals:
            x.update({'ticker': ticker})

        # Add coin signals to the primary signal list
        signals.extend(coin_signals)

    # Re-order signals by index opened
    signals = sorted(signals, key=lambda x: x['index_opened'])
    portfolio = Portfolio(tp_pcts)

    indices_tp_hit = set(itertools.chain.from_iterable(map(lambda x: x['index_tp_hit'], signals)))
    if None in indices_tp_hit:
        indices_tp_hit.remove(None)
    indices_opened = set(map(lambda x: x['index_opened'], signals))
    indices_closed = set(map(lambda x: x['index_closed'], signals))
    indices_of_action = set(sorted(indices_opened | indices_tp_hit | indices_closed))

    for index_of_action in indices_of_action:

        # Opening positions
        while len(signals) > 0 and signals[0]['index_opened'] == index_of_action:
            portfolio.open(signals.pop(0))

        # Selling positions
        if index_of_action in indices_tp_hit:
            for position in filter(lambda x: index_of_action in x['index_tp_hit'], portfolio.positions):
                while index_of_action in position['index_tp_hit']:
                    portfolio.sell(position, index_of_action)

        # Closing positions
        if index_of_action in indices_closed:
            for position in list(filter(lambda x: index_of_action == x['index_closed'], portfolio.positions))[::-1]:
                portfolio.close(position)

    results[cushion] = portfolio.available_capital

results.to_csv('/home/carter/peter-signal/backtests/crypto/cushion.csv')

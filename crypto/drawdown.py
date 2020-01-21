# Calculating max drawdown over a month rolling window
from functions import *
from portfolio import Portfolio

import itertools
import os

from pprint import pprint


tp_pcts = [1, .05, .95, 0, 0]
avgs = [21, 30, 55]
signals = []

for f in os.listdir('../data/binance/'):

    df = pd.read_csv('../data/binance/' + f)
    coin_signals = find_signals(df)

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

p = Portfolio(tp_pcts)

p_snapshot = []


indices_tp_hit = set(itertools.chain.from_iterable(map(lambda x: x['index_tp_hit'], signals)))
indices_tp_hit.remove(None)
indices_opened = set(map(lambda x: x['index_opened'], signals))
indices_closed = set(map(lambda x: x['index_closed'], signals))
indices_of_action = sorted(indices_opened | indices_tp_hit | indices_closed)


for hr in range(len(df)):

    if hr in indices_of_action:
        # Opening positions
        while len(signals) > 0 and signals[0]['index_opened'] == hr:
            p.open(signals.pop(0))

        # Selling positions
        if hr in indices_tp_hit:
            for position in filter(lambda x: hr in x['index_tp_hit'], p.positions):
                while hr in position['index_tp_hit']:
                    p.sell(position, hr)

        # Closing positions
        if hr in indices_closed:
            for position in list(filter(lambda x: hr == x['index_closed'], p.positions))[::-1]:
                p.close(position)

    # Combine available_capital and value of trades to total capital
    available_capital = p.available_capital
    # 1. Check if positions are open to add back values of trades to available_capital
    if p.has_open_positions():
        # Add back each current trade value
        capital_locked_in_trades = sum([
            trade['dollar_value'] * trade['pct_open'] / p.x_leverage \
            for trade in p.positions
        ])
    else:  # No trades open
        capital_locked_in_trades = 0

    # Add snapshot of current portfolio
    p_snapshot.append({
        'date': df['date'].iat[hr],
        'available_capital': available_capital,
        'capital_locked_in_trades': capital_locked_in_trades,
        'total_capital': available_capital + capital_locked_in_trades,
        'trades_open': len(p.positions)
    })


# Save all snapshots
pd.DataFrame(p_snapshot).to_csv('../backtests/crypto/drawdown.csv', index=False)

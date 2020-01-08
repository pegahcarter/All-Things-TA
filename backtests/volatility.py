# Measuring highest draw down over 30 days
# Base code for compounding
from functions import *
from portfolio import Portfolio
import itertools
import os

tp_pcts = [1, .05, .95, 0, 0]

df_totals = pd.DataFrame()

params = [{'colname': 'A',
           'trade_min': 0,
           'trade_max': 1,
           'custom': False},
          {'colname': 'B',
           'trade_min': 0,
           'trade_max': 1,
           'custom': True},
           {'colname': 'C',
            'trade_min': 0.0075,
            'trade_max': 0.04,
            'custom': True}]

for param in params:
    signals = []
    for f in os.listdir('../data/binance/'):

        coin_df = pd.read_csv('../data/binance/' + f)
        coin_signals = find_signals(coin_df, 21, 30, 50, **param)

        # Add `tp`, `index_tp_hit`, and `index_closed`
        determine_TP(coin_df, coin_signals)

        # Add ticker to signal & remove unused keys
        ticker = f[:f.find('.')]
        for x in coin_signals:
            x.update({'ticker': ticker})

        # Add coin signals to the primary signal list
        signals.extend(coin_signals)

    # Re-order signals by index opened
    signals = sorted(signals, key=lambda x: x['index_opened'])

    indices_tp_hit = set(itertools.chain.from_iterable(map(lambda x: x['index_tp_hit'], signals)))
    indices_tp_hit.remove(None)
    indices_opened = set(map(lambda x: x['index_opened'], signals))
    indices_closed = set(map(lambda x: x['index_closed'], signals))
    indices_of_action = set(sorted(indices_opened | indices_tp_hit | indices_closed))

    running_available_capital = []
    p = Portfolio(tp_pcts)

    for index_of_action in range(len(coin_df)):

        if index_of_action in indices_of_action:
            # Open positions
            while len(signals) > 0 and signals[0]['index_opened'] == index_of_action:
                p.open(signals.pop(0))

            # Sell positions
            if index_of_action in indices_tp_hit:
                for position in filter(lambda x: index_of_action in x['index_tp_hit'], p.positions):
                    while index_of_action in position['index_tp_hit']:
                        p.sell(position, index_of_action)

            # Close positions
            if index_of_action in indices_closed:
                for position in list(filter(lambda x: index_of_action == x['index_closed'], p.positions))[::-1]:
                    p.close(position)

        # Append running total
        running_available_capital.append(p.available_capital)

    # Save results to column
    df_totals[param['colname']] = running_available_capital

df_totals.to_csv('../backtests/results/available_capital.csv', index=False)

from TAcharts.py.ta import rolling
from datetime import datetime

df_max_drawdown = pd.DataFrame(index=df_totals.columns, columns=['Max Drawdown %', 'Max Drawdown Date'])


for col in df_totals:
    roll_min = rolling(df_totals[col], n=30*24, fn='min')
    roll_max = rolling(df_totals[col], n=30*24, fn='max')

    delta = np.nan_to_num((roll_max - roll_min) / roll_max, 0)

    max_drawdown_pct = str(round(max(delta) * 100, 1)) + '%'
    max_drawdown_date = coin_df['date'][np.argmax(delta)]
    max_drawdown_date = max_drawdown_date[:max_drawdown_date.find('.000')]

    df_max_drawdown.loc[col] = max_drawdown_pct, max_drawdown_date

df_max_drawdown.to_csv('../backtests/results/max_drawdown.csv')

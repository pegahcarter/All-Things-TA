# Builds on compounding-1.py by finding best combination of additional parameters
# given a set moving average combo and tp
# Finds compounding results with different moving averages and tp_pct
from functions import *
from portfolio import Portfolio
from variables import avgs_combined, tp_pcts_list
import itertools
import os
import ujson
from tqdm import tqdm

df_list = {}
for f in os.listdir('../data/binance/'):
    ticker = f[:f.find('.')]
    df_list[ticker] = pd.read_csv('../data/binance/' + f)


tp_pcts = [1, .05, .95, 0, 0]

num_candles_list = range(2, 11)
median_multiplier_list = range(2, 11)
sdev_multiplier_list = range(6, 25, 2)
window_lookback_list = [24, 36, 48, 60, 72]


results = pd.DataFrame()

for window_lookback in window_lookback_list:

    print('\n' + str(window_lookback) + '\n')
    results_for_window = {}

    for num_candles in tqdm(num_candles_list):
        for median_multiplier in median_multiplier_list:
            for sdev_multiplier in sdev_multiplier_list:

                signals = []

                for ticker, df in df_list.items():
                    coin_signals = find_signals(
                        df, 21, 30, 50, num_candles=num_candles, median_multiplier=median_multiplier,
                        sdev_multiplier=sdev_multiplier, window_lookback=window_lookback
                    )

                    # Add `tp`, `index_tp_hit`, and `index_closed`
                    determine_TP(df, coin_signals)

                    # Add ticker to signal & remove unused keys
                    for x in coin_signals:
                        x.update({'ticker': ticker})

                    # Add coin signals to the primary signal list
                    signals.extend(coin_signals)

                # Re-order signals by index opened
                signals = sorted(signals, key=lambda x: x['index_opened'])

                indices_tp_hit = set(itertools.chain.from_iterable(map(lambda x: x['index_tp_hit'], signals)))
                if None in indices_tp_hit:
                    indices_tp_hit.remove(None)
                indices_opened = set(map(lambda x: x['index_opened'], signals))
                indices_closed = set(map(lambda x: x['index_closed'], signals))
                indices_of_action = sorted(indices_opened | indices_tp_hit | indices_closed)

                portfolio = Portfolio(tp_pcts)

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


                results_for_window['-'.join([str(num_candles), str(median_multiplier), str(sdev_multiplier)])] = portfolio.available_capital

    # Save ending portfolio value
    results[window_lookback] = results_for_window

results.to_csv('/home/carter/peter-signal/data/compounding_2.csv')

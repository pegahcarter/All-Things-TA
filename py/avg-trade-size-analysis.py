# Analyzing the percent/number of trades taken from reducing trade size criteria
# to between .75% and 4%

# Could you provide a trade log in this style: pair - buy price - sell price - % profit or loss
import os
from functions import *
import seaborn as sns
from datetime import timedelta


tps = {0: -1, 1: 0.025, 2: 0.95, 3: 0.95, 4: 0.95}


def all_signals(trade_min, trade_max, custom=True, directory='../data/binance/', cushion=0):
    signals = []
    for f in os.listdir(directory):
        ticker = f[:f.find('.')]
        df = pd.read_csv(directory + f)

        coin_signals = find_signals(df, 21, 30, 55, trade_min, trade_max, custom, cushion)

        # Add `tp`, `index_tp_hit`, and `index_closed`
        determine_TP(df, coin_signals)

        # Add ticker to signal & remove unused keys
        for x in coin_signals:
            x.update({'ticker': ticker})

        # Add coin signals to the primary signal list
        signals.extend(coin_signals)

    # Re-order signals by index opened
    signals = sorted(signals, key=lambda x: x['index_opened'])
    signals = pd.DataFrame(signals)


    signals['date_opened'] = pd.to_datetime(signals['date'])
    hrs_open = signals['index_closed'] - signals['index_opened']

    signals['date_closed'] = [signals['date_opened'][i] + timedelta(hours=int(hrs_open[i])) for i in range(len(signals))]
    signals['net_profit'] = [signals['pct'][i] * tps[signals['tp'][i]] for i in range(len(signals))]
    return signals[['ticker', 'price', 'stop_loss', 'net_profit', 'pct', 'tp']]


df_all = all_signals(0, 1, custom=False)
df_custom = all_signals(.0075, .04, custom=True)

df_all.to_csv('../backtests/crypto/trades_without_custom_logic.csv', index=False)
df_custom.to_csv('../backtests/crypto/trades_with_custom_logic.csv', index=False)



df_all['tp'].value_counts() / len(df_all)
df_custom['tp'].value_counts() / len(df_custom)








df_crypto = df_crypto[['ticker', 'pct', 'tp']]

    ticker_pct_sorted = df[df['ticker'] == ticker]['pct'].sort_values().values


df_crypto_outliers = df_crypto[(df_crypto['pct'] < .0075) | (df_crypto['pct'] > .04)]



df_crypto.sort_values('pct', ascending=False)[:15]

df_crypto['pct'].describe()



df_crypto['tp'].value_counts(sort=False) / len(df_crypto)

removed_top_pct = sum(df_crypto['pct'] > .04) / len(df_crypto)
removed_bottom_pct = sum(df_crypto['pct'] < .0075) / len(df_crypto)


sns.distplot(df_crypto['pct'])

#  TODO: Remove 5% of signals on


df_fx = all_signals(0, .8, directory='../data/oanda/')

df_fx['ticker'].value_counts()

sns.distplot(df_fx['pct'])

sum(df_fx['pct']


df_fx['pct']


# for ticker in df_crypto['ticker'].unique():
#     sns.distplot(df_crypto[df_crypto['ticker'] == ticker]['pct'], kde=True, label=ticker)

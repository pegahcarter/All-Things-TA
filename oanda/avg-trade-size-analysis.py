# Analyzing the percent/number of trades taken from reducing trade size criteria
# to between .75% and 4%

import os
from functions import *
import seaborn as sns


tps = {0: -1, 1: 0.025, 2: 0.925, 3: 0.925, 4: 0.925}


def all_signals(trade_min, trade_max, directory='../data/binance/'):
    signals = []
    for f in os.listdir(directory):
        ticker = f[:f.find('.')]
        df = pd.read_csv(directory + f)

        coin_signals = find_signals(df, 21, 30, 50, trade_min, trade_max)

        # Add `tp`, `index_tp_hit`, and `index_closed`
        determine_TP(df, coin_signals)

        # Add ticker to signal & remove unused keys
        for x in coin_signals:
            x.update({'ticker': ticker})

        # Add coin signals to the primary signal list
        signals.extend(coin_signals)

    # Re-order signals by index opened
    signals = sorted(signals, key=lambda x: x['index_opened'])
    return pd.DataFrame(signals)


df_crypto = all_signals(0, .8)
df_crypto = df_crypto[['ticker', 'pct', 'tp']]
# ------------------------------------------------------------------------------
# Net profit (the old fashioned way)





# ------------------------------------------------------------------------------

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

import TAcharts
import os

import pandas as pd
import numpy as np


np.array()


os.listdir('../data')


btc = pd.read_csv('../data/binance/BTC-USDT.csv')

btc.head()
btc['date'] = pd.to_datetime(btc['date'])

btc['date'].iloc[-1]


btc['pct_change'] = (btc['high'] - btc['low']) / btc['open']
btc['hr'] = btc['date'].apply(lambda x: x.hour)

btc.groupby('hr')['pct_change'].mean().sort_values(ascending=False)

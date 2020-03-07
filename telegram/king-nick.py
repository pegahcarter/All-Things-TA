from datetime import datetime
import pandas as pd
import numpy as np
import sys
from TAcharts.indicators import sdev, rolling

# Read in data
ltc = pd.read_csv('data/LTC-BTC.csv')[['date', 'open', 'close', 'volume']]
btc = pd.read_csv('data/BTC-USDT.csv')[['date', 'open', 'close', 'volume']]


# Add columns
ltc['pct_change'] = (ltc['close'] - ltc['open']) / ltc['open']
# btc['pct_change'] = (btc['close'] - btc['open']) / btc['open']

# ltc['rolling_pct_change'] = np.cumsum(ltc['pct_change'])

# Minimum value of top 10% of pct_change candles
top_2pct_change = ltc['pct_change'].sort_values()[int(len(ltc) * .98)]


# Feb 7, 2019 at 9pm
ltc_halving_pump = ltc.loc[ltc['date'] >= '2019-02-07 21:00:00'].reset_index(drop=True)[:60*24]


ltc_halving_pump_top = ltc_halving_pump[ltc_halving_pump['pct_change'] > top_2pct_change]
ltc_halving_pump_top[:10]


# Convert /BTC to /USD for alts
btc_price = btc['open']

btc['volume_usd'] = btc_price * btc['volume']
ltc['volume_usd'] = ltc['open'] * btc_price * ltc['volume']
eos['volume_usd'] = eos['open'] * btc_price * eos['volume']
eth['volume_usd'] = eth['open'] * btc_price * eth['volume']

btc['alt_volume_usd'] = ltc['volume_usd'] + eos['volume_usd'] + eth['volume_usd']

btc.head()

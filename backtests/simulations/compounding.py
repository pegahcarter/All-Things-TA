# This file will simulate a portfolio and return the end total value.
# Hopefully, the gains will compound and we'll see a higher ending value than
#   just the %

import numpy as np
import pandas as pd
from py.functions import *

df = pd.read_csv('ohlcv/BTC.csv')
signals = find_signals(df)

# Step 1: figure out how long the position is open
tp, index_tp_hit = determine_TP(df, signals, cushion=0.003, compound=True)
signals['tp'] = tp
signals['index_tp_hit'] = index_tp_hit

signals['hrs_position_open'] = np.subtract(index_tp_hit, signals.index)

signals.head()

portfolio_value = 1000.
trade_size = .05

# This file will simulate a portfolio and return the end total value.
# Hopefully, the gains will compound and we'll see a higher ending value than
#   just the %

import numpy as np
import pandas as pd
from py.functions import *

df = pd.read_csv('ohlcv/ETH.csv')
signals = find_signals(df)

# Step 1: figure out how long the position is open
tp, index_tp_hit = determine_TP(df, signals, compound=True)
signals = signals.reset_index()

signals['tp'] = tp
signals['hrs_position_open'] = np.subtract(index_tp_hit, signals['index'])


# Step 2: figure out the most # of positions open at one time
signals['total_positions_open'] = [sum(signals['index'][i] + signals['hrs_position_open'][i] > signals['index'][i:]) for i in signals.index]

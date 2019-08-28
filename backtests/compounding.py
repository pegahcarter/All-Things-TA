# This file will simulate a portfolio and return the end total value.
# Hopefully, the gains will compound and we'll see a higher ending value than
#   just the %

import numpy as np
import pandas as pd
from py.functions import *

df = pd.read_csv('ohlcv/BTC.csv')
signals = find_signals(df)
signals['tp'] = determine_TP(df, signals, cushion=0.003)

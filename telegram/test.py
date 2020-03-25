# Correlation between BTC and LTC for top 1% of candles, looping through parameters
from datetime import datetime
import pandas as pd
import numpy as np
from group_candles import group_candles

# ------------------------------------------------------------------------------------
# Variables to loop through

candle_periods = [1, 3, 5, 15]
delay_periods = [1, 2, 3, 5]
btc_window_periods = [1, 2, 3, 5, 6]

# ------------------------------------------------------------------------------------


# Read in data
ltc = pd.read_csv('data/LTC-BTC.csv')
btc = pd.read_csv('data/BTC-USDT.csv')

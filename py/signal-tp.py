from functions import find_signals, determine_TP
from portfolio import Portfolio
import itertools
import os
import pandas as pd

tp_pcts = [1, .05, .95, 0, 0]

signals = pd.read_csv('../data/signals/atta_insiders.csv')

signals.head()

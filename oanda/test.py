# File used to test different shit
# df = pd.read_csv('/home/carter/peter-signal/data/oanda/AUD-USD.csv')

from signals import signals
import pandas as pd

df = pd.DataFrame(signals())
df.head()

# ----------------------------------------------------------------------------
# TEST: Load requirements, and pass requirement param into a function
#   similar to `base()`
trade_req = pd.read_csv('/home/carter/peter-signal/backtests/oanda/requirements.csv', index='ticker')

trade_req

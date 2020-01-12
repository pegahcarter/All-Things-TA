# File used to test different shit
# df = pd.read_csv('/home/carter/peter-signal/data/oanda/AUD-USD.csv')
from signals import signals
import pandas as pd

df = pd.DataFrame(signals(tp=True))

df['tp'].value_counts(sort=False) / len(df)



len(df)
df.head(2)

# ----------------------------------------------------------------------------
# TEST: Load requirements, and pass requirement param into a function
#   similar to `base()`
trade_req = pd.read_csv('/home/carter/peter-signal/backtests/oanda/requirements.csv').set_index('ticker').to_dict(orient='index')

ticker = 'EUR-USD'

trade_req[ticker]

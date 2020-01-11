# Test file to create signals for tickers
# df = pd.read_csv('/home/carter/peter-signal/data/oanda/AUD-USD.csv')

from signals import signals
import pandas as pd

df = pd.DataFrame(signals())
df.head()

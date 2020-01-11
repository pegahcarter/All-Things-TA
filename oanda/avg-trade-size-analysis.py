# Analyzing the percent/number of trades taken from reducing trade size criteria

from signals import signals
import pandas as pd
import seaborn as sns
import numpy as np

# Since we removed top 5% and bottom 10% for crypto, I'll use the same method for FX
# However, it needs to be applied uniquely to each ticker

df = pd.DataFrame(signals())
requirements = {}

for ticker in set(df['ticker']):
    ticker_pct_sorted = df[df['ticker'] == ticker]['pct'].sort_values().values

    # Bottom 10% of trades
    trade_min = ticker_pct_sorted[int(len(ticker_pct_sorted) * .10)]
    # Top 5% of trades
    trade_max = ticker_pct_sorted[-int(len(ticker_pct_sorted) * .05)]

    requirements[ticker] = {'trade_min': trade_min, 'trade_max': trade_max}


df_requirements = pd.DataFrame().from_dict(requirements, orient='index')
df_requirements.to_csv('/home/carter/peter-signal/backtests/oanda/requirements.csv')

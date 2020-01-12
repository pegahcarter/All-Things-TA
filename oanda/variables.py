import pandas as pd


trade_size_dict = pd.read_csv('/home/carter/peter-signal/backtests/oanda/requirements.csv').set_index('ticker').to_dict(orient='index')

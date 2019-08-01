import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import ccxt


x = ccxt.binance()
btc = np.array(x.fetch_ohlcv('BTC/USDT', '1h', limit=200))[:, [0,4]]

df = pd.DataFrame(btc, columns=['date', 'BTC/USD'])

for coin in ['ETH', 'XRP', 'EOS', 'BCH', 'LTC', 'BNB']:
    ticker = coin + '/BTC'
    df[ticker] = np.array(x.fetch_ohlcv(ticker, '1h', limit=200))[:, 4]/df['BTC/USD']
df.head()





df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
df['date'] /= 1000

df['date'] = [datetime.fromtimestamp(x) for x in df['date']]
df.head()












from py.variables import *
from urllib.parse import urlencode

url = 'https://api.telegram.org/bot' + API_KEY + '/sendMessage?'
mydict = {'chat_id': CHAT_ID, 'text': 'Hello'}
url + urlencode(mydict)

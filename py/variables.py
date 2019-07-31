import ccxt
import pandas as pd
from datetime import datetime, timedelta
import time

binance = ccxt.binance()

since = datetime.now() - timedelta(hours=500)
since = int(time.mktime(since.timetuple())*1000)

# tickers = ['BTC/USD', 'ETH/USD', 'ETHU19', 'BCHU19', 'XRPU19', 'LTCU19', 'EOSU19']
tickers = ['BTC/USDT', 'ETH/USDT', 'ETH/BTC', 'BCH/BTC', 'XRP/BTC', 'LTC/BTC', 'EOS/BTC']
candle_intervals = {
    '1h': 'Hourly',
    '1d': 'Daily'
}

API = '862004249:AAFS3xQAWRCYVbadZqr94k3sA5oqyjzmMW8'
url = 'https://api.telegram.org/bot' + API + '/sendMessage?'
chat_id = '-360419097'

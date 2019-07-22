import ccxt
import pandas as pd
from datetime import datetime, timedelta
import time

bitmex = ccxt.bitmex()

since = datetime.now() - timedelta(hours=500)
since = time.mktime(since.timetuple())*1000

tickers = ['BTC/USD', 'ETH/USD', 'ETHU19', 'XRPU19', 'LTCU19', 'EOSU19']

API = '862004249:AAFS3xQAWRCYVbadZqr94k3sA5oqyjzmMW8'
url = 'https://api.telegram.org/bot' + API + '/sendMessage?'
chat_id = '-360419097'

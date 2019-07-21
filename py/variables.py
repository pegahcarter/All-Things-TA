import ccxt
import pandas as pd
from datetime import datetime, timedelta
import time

bitmex = ccxt.bitmex()


since = datetime.now() - timedelta(hours=500)
since = time.mktime(since.timetuple())*1000

tickers = ['BTC/USD', 'ETH/USD', 'XRPU19', 'LTCU19', 'EOSU19']

API_KEY = '862004249:AAFS3xQAWRCYVbadZqr94k3sA5oqyjzmMW8'
CHAT_ID = '-360419097'

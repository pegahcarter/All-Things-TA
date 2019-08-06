import ccxt
import pandas as pd
from datetime import datetime, timedelta
import time
from google import g_doc

since = datetime.now() - timedelta(hours=500)
since = int(time.mktime(since.timetuple())*1000)

binance = ccxt.binance()

candle_intervals = {
    '1h': 'Hourly',
    '1d': 'Daily'
}

# Telegram
API = '862004249:AAFS3xQAWRCYVbadZqr94k3sA5oqyjzmMW8'
url = 'https://api.telegram.org/bot' + API + '/sendMessage?'
chat_id = '-360419097'

tick_sheet = g_doc.worksheet_by_title('Crypto Tickers')
tickers = [str(ticker) for ticker in tick_sheet.get_col(2) if len(ticker) > 0 and ticker != 'Tickers']

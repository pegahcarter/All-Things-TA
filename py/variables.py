from datetime import datetime, timedelta
import time
import pygsheets
import ccxt
import os

since = datetime.now() - timedelta(hours=500)
since = int(time.mktime(since.timetuple())*1000)

exchange = ccxt.bitfinex()

candle_intervals = {
    '1h': 'Hourly',
    '1d': 'Daily'
}

# Telegram
API = '862004249:AAFS3xQAWRCYVbadZqr94k3sA5oqyjzmMW8'
url = 'https://api.telegram.org/bot' + API + '/sendMessage?'
chat_id = '-360419097'
test_chat_id = '-1001192596591'
signal_chat_id = '-1001350840772'

# Google docs
gc = pygsheets.authorize(service_file='/home/carl/Documents/crypto/peter-signal/credentials.json')
g_doc = gc.open_by_key('1T67gVealvVutn_VuiedbH7ViK8_OIBWOmoDIMq82oQE')

tick_sheet = g_doc.worksheet_by_title('Tickers')
tickers = [str(ticker) for ticker in tick_sheet.get_col(2) if len(ticker) > 0 and ticker != 'Tickers']

def get_gsheet(candle_string):
    return g_doc.worksheet_by_title(candle_string).get_as_df()

def save_gsheet(candle_string, df):
    return g_doc.worksheet_by_title(candle_string).set_dataframe(df, (1,1))

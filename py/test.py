import ccxt
bitmex = ccxt.bitmex()
bitmex.fetch_ticker('XRPU19')

from py.variables import *
from urllib.parse import urlencode

url = 'https://api.telegram.org/bot' + API_KEY + '/sendMessage?'
mydict = {'chat_id': CHAT_ID, 'text': 'Hello'}
url + urlencode(mydict)

import ccxt

# exchange = ccxt.bitfinex()
exchange = ccxt.bitmex()


# Telegram
API = '862004249:AAFS3xQAWRCYVbadZqr94k3sA5oqyjzmMW8'
url = 'https://api.telegram.org/bot' + API + '/sendMessage?'
chat_id = '-360419097'
test_chat_id = '-1001192596591'
wc_id = '@worldclasstrader'
wc_elite_id = '-1001229157672'
atta_id = '@AllthingsTA'
atta_insiders_id = '-1001456456400'


channels = {
    'wc_elite': [21, 30, 50],
    'atta_insiders': [8, 25, 50]
}

tickers = ['BTC/USD', 'ETH/USD', 'ETHZ19', 'LTCZ19', 'XRPZ19', 'BCHZ19', 'EOSZ19']

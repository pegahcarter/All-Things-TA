import ccxt

# exchange = ccxt.bitfinex()
exchange = ccxt.bitmex()


# Telegram
API = '862004249:AAFS3xQAWRCYVbadZqr94k3sA5oqyjzmMW8'
url = 'https://api.telegram.org/bot' + API + '/sendMessage?'
chat_id = '-360419097'
test_chat_id = '-1001192596591'
world_class = '@worldclasstrader'

tickers = ['BTC/USD', 'ETH/USD', 'ETHZ19', 'LTCZ19', 'XRPZ19', 'BCHZ19', 'EOSZ19']


channels = [
    {
        'name': 'world_class_elite',
        'chat_id': '-1001229157672',
        'averages': [21, 30, 50]
    },
    {
        'name': 'atta_insiders',
        'chat_id': '-1001456456400',
        'averages': [8, 25, 50]
    }
]

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


tickers = ['BTC/USD', 'ETH/USD', 'ETHZ19', 'LTCZ19', 'XRPZ19', 'BCHZ19', 'EOSZ19']


avg1 = [5, 8, 10, 13, 15, 21]
avg2 = [13, 15, 21, 25, 30, 34, 40, 55, 60, 75, 89]
avg3 = [34, 40, 50, 55, 60, 75, 89, 100, 144, 150, 200, 233]
avgs_combined = [[a1, a2, a3] for a1 in avg1 for a2 in avg2 for a3 in avg3 if a1 < a2 and a2 < a3]

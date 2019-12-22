import ccxt
from itertools import permutations


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


tickers = ['BTC/USD', 'ETH/USD', 'ETHH20', 'LTCH20', 'XRPH20', 'BCHH20', 'EOSH20']


avg1 = [8, 15, 21, 30]
avg2 = [21, 25, 30, 34, 40, 55, 60]
avg3 = [34, 40, 50, 55, 60, 75, 89, 100, 144]
avgs_combined = [[a1, a2, a3] for a1 in avg1 for a2 in avg2 for a3 in avg3 if a1 < a2 and a2 < a3]


pcts = list(range(0, 101, 10))
pcts *= 4
perms = permutations(pcts, 4)

tp_pcts = set([x for x in perms if sum(x) == 100])
tp_pcts_lst = []

for tp_pct in tp_pcts:
    tp_pcts_lst.append(dict(zip(range(1,5), tp_pct)))

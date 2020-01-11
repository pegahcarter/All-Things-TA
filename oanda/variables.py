import ccxt
from itertools import permutations
import numpy as np

exchange = ccxt.bitmex()

tickers = ['BTC/USD', 'ETH/USD', 'ETHH20', 'LTCH20', 'XRPH20', 'BCHH20', 'EOSH20']


# Telegram
API = '862004249:AAFS3xQAWRCYVbadZqr94k3sA5oqyjzmMW8'
url = 'https://api.telegram.org/bot' + API + '/sendMessage?'
chat_id = '-360419097'
test_chat_id = '-1001192596591'
wc_id = '@worldclasstrader'
wc_elite_id = '-1001229157672'
atta_id = '@AllthingsTA'
atta_insiders_id = '-1001456456400'


# Moving average combinations
avg1 = [8, 15, 21, 30]
avg2 = [21, 25, 30, 34, 40, 55, 60]
avg3 = [34, 40, 50, 55, 60, 75, 89, 100, 144]
avgs_combined = [[a1, a2, a3] for a1 in avg1 for a2 in avg2 for a3 in avg3 if a1 < a2 and a2 < a3]


# Creating TP pct ranges
pcts = list(np.arange(11)/10) * 4
perms = set(permutations(pcts, 4))

tp_pcts_list = [list(x) for x in perms if sum(x) == 1]

for tp_pcts in tp_pcts_list:
    tp_pcts.insert(0, 1)

from functions import *
import pandas as pd
import numpy as np
import itertools
import os

# --------------------------------------------------------------------------------
# 2019.01.01
# Seeing the best results of compounding-2.py
df = pd.read_csv('../backtests/results/compounding-2.csv')
df.columns
df.sort_values('ending_capital', ascending=False)[:10]


# --------------------------------------------------------------------------------
# 2019.12.29
# Testing out new portfolio class with revised determine_TP
df = pd.read_csv('../data/binance/BTC-USDT.csv')

%timeit signals = find_signals(df, window_fast=21, window_mid=30, window_slow=55)
76.4 ms ± 759 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)

%timeit x = determine_TP(df, signals)
1.05 ms ± 3.7 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

results = set(itertools.chain.from_iterable(map(lambda x: x['index_tp_hit'], signals)))
results.remove(None)

index_opened = set(map(lambda x: x['index_opened'], signals))
len(index_opened)
test = sorted(results | index_opened)
test
len(test)
indices_with_action = index_opened.update(results)



# --------------------------------------------------------------------------------
# 2019.12.28
# Figuring out argsort of top 3


df = pd.read_csv('../data/bitmex/BTCUSD.csv')

close_pd = df['close']
close_np = df['close'].values


def original_fn():
    body_sorted = sorted(close_pd[500:548])
    results = sum(body_sorted[-3:])
    return

def new_fn():
    body_sorted = np.sort(close_np[500:548])
    results = np.sum(body_sorted[-3:])
    return results


%timeit original_fn()
58.1 µs ± 1.36 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)


%timeit new_fn()
6.17 µs ± 43.2 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

# --------------------------------------------------------------------------------
# I need to create a ticker column/data point

all_signals = []
tp_pcts = {1: 10, 2: 10, 3: 10, 4: 70}

for f in os.listdir('../data/binance/'):

    df = pd.read_csv('../data/binance/' + f)
    signals = find_signals(df, 21, 30, 50)
    determine_TP(df, signals)

    for x in range(len(signals)):
        signals[x]['ticker'] = f[:f.find('.')]

    all_signals.extend(signals)

net_profit(all_signals, tp_pcts)


len(all_signals)

819, 1.62



test = list(sorted(all_signals, key=lambda x: x['index_opened']))
test[:4]



# --------------------------------------------------------------------------------

gc = pygsheets.authorize(service_file='C:/Users/carter/Documents/crypto/peter-signal/credentials.json')
g_doc = gc.open_by_key('1T67gVealvVutn_VuiedbH7ViK8_OIBWOmoDIMq82oQE')

tick_sheet = g_doc.worksheet_by_title('Tickers')
tickers = [str(ticker) for ticker in tick_sheet.get_col(2) if len(ticker) > 0 and ticker != 'Tickers']

def get_gsheet(candle_string):
    return g_doc.worksheet_by_title(candle_string).get_as_df()

def save_gsheet(candle_string, df):
    return g_doc.worksheet_by_title(candle_string).set_dataframe(df, (1,1))

# ------------------------------------------------------------------------------
def foo():
    data = [[1,1,1], [2,3,4], [10, 100, 1000]]
    # df = pd.DataFrame(data*i, columns=['col1', 'col2', 'col3'])
    return data

test1_a = []
for i in range(3):
    test1_a += foo()
test1_a

test1_b = [foo() for i in range(3)]
test1_b

# --------------------------------------------------------------------------------
def foo2():
    data = [[1,1,1], [2,3,4], [10, 100, 1000]]
    return pd.DataFrame(data, columns=['col1', 'col2', 'col3'])

test2_a = pd.DataFrame([])
for i in range(3):
    test2_a = test2_a.append(foo())
test2_a

test2_b = [foo2() for i in range(3)]
test2_b
len(test2_b)

test2_c = pd.DataFrame(columns=['col1', 'col2', 'col3'])
test2_c = test2_c.append([foo2() for i in range(3)], ignore_index=True)
test2_c


test2_d = pd.DataFrame(columns=['col1', 'col2', 'col3'])
test2_d = test2_d.append([foo() for i in range(3)], ignore_index=True)
test2_d

test3_a = pd.DataFrame([foo() for i in range(3)], columns=['col1', 'col2', 'col3'])
test3_a

test3_b = pd.DataFrame([])

data = requests.get('https://api.telegram.org/bot862004249:AAFS3xQAWRCYVbadZqr94k3sA5oqyjzmMW8/getUpdates').json()['result']

messages = list(filter(lambda x: 'channel_post' in x.keys(), data))

url = 'https://api.telegram.org/bot862004249:AAFS3xQAWRCYVbadZqr94k3sA5oqyjzmMW8/sendMessage?'
requests.get(url + urlencode({'chat_id': '@worldclasstrader', 'text': 'Test'}))

requests.get(url + urlencode({'chat_id': wc_id, 'text': 'Test'}))
response = requests.get(url + urlencode({'chat_id': atta_id, 'text': 'Test'}))

response.text



# --------------------------------------------------------------------------------
df = pd.read_csv(os.getcwd() + '/data/optimize_moving_avg.csv')

df.head()

df['average'] = df['average'].map(lambda row: row[1:-1].split(', '))
avgs = [list(map(lambda n: int(n), avg)) for avg in df['average']]



df['mean'] = df.drop('average', axis=1).mean(axis=1)
df['sum'] = df.drop('average', axis=1).sum(axis=1)

df2 = df[['average', 'mean', 'sum']]
df2 = df2.sort_values('sum', ascending=False).reset_index(drop=True)
df2[:60]

# --------------------------------------------------------------------------------
df = pd.read_csv('data/bitfinex/BTC.csv')

df['test'] = numpy_ewm_alpha_v2(df['close'], 14)

def numpy_ewm_alpha_v2(data, window):
    alpha = 2. / (window + 1)
    wghts = (1-alpha)**np.arange(window)
    wghts /= wghts.sum()
    out = np.convolve(data,wghts)
    out[:window-1] = np.nan
    return out[:data.size]


def ewma(data, window):
    a = 2. / (window + 1)
    a_inverse = 1 - a
    n = data.shape[0]

    pows = a_inverse**(np.arange(n+1))

    scale_arr = 1. / pows[::-1]
    offset = data[0] * pows[1:]
    pw0 = a * a_inverse**(n-1)

    mult = data * pw0 * scale_arr
    cumsums = mult.cumsum()
    results = offset + cumsums*scale_arr[::-1]
    return results

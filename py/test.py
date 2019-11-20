import requests
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import ccxt
from py.utils import *



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

%timeit prices = df['close'].to_numpy()
%timeit prices = np.array(df['close'])



df['test'] = numpy_ewm_alpha_v2(df['close'], 14)

df.iloc[-14:]




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

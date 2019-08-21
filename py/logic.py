import pandas as pd
import numpy as np
from variables import tickers
import requests
from urllib.parse import urlencode


def run(candle_abv):
    signal_df = pd.DataFrame()
    for ticker in tickers:
        if candle_abv == '1h':
            df = exchange.fetch_ohlcv(ticker, candle_abv, limit=500, since=since)
        else:
            df = exchange.fetch_ohlcv(ticker, candle_abv, limit=500)

        df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])

        signals = find_signals(df)
        signals['ticker'] = ticker
        signal_df = signal_df.append(signals, ignore_index=True)

    signal_df['date'] = [datetime.fromtimestamp(x/1000) for x in signal_df['date']]
    signal_df = signal_df.sort_values('date').reset_index(drop=True)
    return signal_df


def send_signal(row, candle_string):

    if candle_string == 'Hourly':
        date = row['date'].strftime('%m/%d %I:%M %p')
        leverage = '10x'
    else:   # candle_string == 'Daily'
        date = row['date'].strftime('%m/%d')
        leverage = '3x'

    diff = row['price'] - row['Stop Loss']
    tp1 = row['price'] + diff/2.
    tp2 = row['price'] + diff
    tp3 = row['price'] + diff*2
    tp4 = row['price'] + diff*3

    if row['ticker'] == 'BTC/USD':
        row['ticker'] = 'XBT/USD'
        row['price'] = int(row['price'])
        row['Stop Loss'] = int(row['Stop Loss'])
        tp1 = int(tp1)
        tp2 = int(tp2)
        tp3 = int(tp3)
        tp4 = int(tp4)
    else:
        if row['ticker'] == 'XRP/BTC':
            decimals = '.8f'
        elif row['ticker'] == 'EOS/BTC':
            decimals = '.7f'
        elif row['ticker'] == 'LTC/BTC':
            decimals = '.6f'
        elif row['ticker'] == 'BCH/BTC':
            decimals = '.5f'
        elif row['ticker'] in ['XRP/USD', 'EOS/USD', 'ETH/BTC']:
            decimals = '.4f'
        else:
            decimals = '.2f'
        row['price'] = format(row['price'], decimals)
        row['Stop Loss'] = format(row['Stop Loss'], decimals)
        tp1 = format(tp1, decimals)
        tp2 = format(tp2, decimals)
        tp3 = format(tp3, decimals)
        tp4 = format(tp4, decimals)

    if row['ticker'] == 'ETH/BTC':
        row['ticker'] = 'ETH/M19'
    elif '/BTC' in row['ticker']:
        row['ticker'] = row['ticker'][:3] + '/U19'

    # text = date + '\n'
    text = candle_string + '\n'
    text += row['ticker'] + '\n'
    text += 'BitMEX\n'
    text += row['signal'] + ' ' + str(row['price']) + '\n'
    text += 'Take profit ' + str(tp1) + ', ' + str(tp2) + ', ' + str(tp3) + ', ' + str(tp4) + '\n'
    text += 'Leverage ' + leverage +  '\n'
    text += 'Stop loss ' + str(row['Stop Loss'])

    requests.get(url + urlencode({'chat_id': test_chat_id, 'text': text}))



def calc_ma(_close, window):
    return _close.rolling(window=window).mean().fillna(0)


def calc_ema(_close, window):
    return _close.ewm(span=window, adjust=False).mean()


def calc_macd(_close, fast=12, slow=26):
    '''
    macd line = fast_ema - slow_ema
    signal line = 9ema of macd line
    histogram = macd line - signal line
    '''
    ema_fast = calc_ema(_close, window=fast)
    ema_slow = calc_ema(_close, window=slow)
    return ema_fast - ema_slow


def calc_rsi(_close):
    n = 14
    deltas = np.diff(_close)
    seed = deltas[:n+1]
    up = seed[seed > 0].sum()/n
    down = -seed[seed < 0].sum()/n
    rsi = np.zeros_like(_close)
    rsi[:n] = 100. - 100./(1.+ up/down)
    for i in range(n, len(_close)):
        delta = deltas[i-1]
        if delta > 0:
            up_val = delta
            down_val = 0
        else:
            up_val = 0
            down_val = -delta

        up = (up*(n-1) + up_val)/n
        down = (down*(n-1) + down_val)/n

        rsi[i] = 100. - 100./(1. + up/down)

    return rsi


# def cross(line1, line2):
#     nan_count = max(line1.isna().sum(), line2.isna().sum())
#     crosses = [False for i in range(nan_count)]
#     l1_gt_l2 = line1 > line2
#     current_val = l1_gt_l2[nan_count]
#     for next_val in l1_gt_l2[nan_count+1:]:
#         crosses.append(current_val != next_val)
#         current_val = next_val
#     crosses.insert(0, False)
#     return crosses

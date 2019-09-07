from variables import *
from functions import *
import pandas as pd
import numpy as np
import requests
from urllib.parse import urlencode
from datetime import datetime, timedelta
import time


def run(candle_abv):
    signal_df = pd.DataFrame()
    for ticker in tickers:
        if candle_abv == '1h':
            limit = 500
            since = datetime.now() - timedelta(hours=limit)
        else:  # candle_abv == '1d'
            limit = 250
            since = datetime.now() - timedelta(days=limit)

        since = int(time.mktime(since.timetuple()) * 1000)
        df = exchange.fetch_ohlcv(ticker, candle_abv, since=since, limit=limit)

        df = pd.DataFrame(df, columns=['date', 'open', 'high', 'low', 'close', 'volume'])

        signals = find_signals(df)
        if len(signals) > 0:
            signals.loc[:, 'ticker'] = ticker
            signal_df = signal_df.append(signals, ignore_index=True, sort=False)

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

    low_price = row['price'] * .999
    high_price = row['price'] * 1.001

    diff = row['price'] - row['stop_loss']
    tp1 = row['price'] + diff/2.
    tp2 = row['price'] + diff
    tp3 = row['price'] + diff*2
    tp4 = row['price'] + diff*3

    if row['ticker'] == 'BTC/USD':
        row['ticker'] = 'XBT/USD'
        # row['price'] = int(row['price'])
        low_price = int(low_price)
        high_price = int(high_price)
        row['stop_loss'] = int(row['stop_loss'])
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
        elif row['ticker'] in ['BCH/BTC', 'ETH/BTC']:
            decimals = '.5f'
        elif row['ticker'] in ['XRP/USD', 'EOS/USD']:
            decimals = '.4f'
        else:
            decimals = '.2f'
        # row['price'] = format(row['price'], decimals)
        low_price = format(low_price, decimals)
        high_price = format(high_price, decimals)
        row['stop_loss'] = format(row['stop_loss'], decimals)
        tp1 = format(tp1, decimals)
        tp2 = format(tp2, decimals)
        tp3 = format(tp3, decimals)
        tp4 = format(tp4, decimals)

    if '/BTC' in row['ticker'] and row['ticker'] != 'ETH/BTC':
        row['ticker'] = row['ticker'][:3] + '/U19'

    text = '🚨🚨🚨\n\n'
    text += row['ticker'] + '\n'
    text += 'BitMEX\n'
    text += row['signal'] + ' zone ' + str(low_price) + '-' + str(high_price) + '\n'
    text += 'Take profit ' + str(tp1) + ', ' + str(tp2) + ', ' + str(tp3) + ', ' + str(tp4) + '\n'
    text += 'Leverage ' + leverage +  '\n'
    text += 'Stop loss ' + str(row['stop_loss']) + '\n\n'
    text += '🚨🚨🚨'


    if row['ticker'] in ['BTC/USD', 'ETH/USD', 'ETH/U19']:
        requests.get(url + urlencode({'chat_id': world_class, 'text': text}))
        requests.get(url + urlencode({'chat_id': world_class_elite, 'text': text}))
    elif row['ticker'] not in ['BCH/USD', 'EOS/USD', 'XRP/USD', 'LTC/USD']:
        requests.get(url + urlencode({'chat_id': world_class_elite, 'text': text}))

    requests.get(url + urlencode({'chat_id': test_chat_id, 'text': text}))

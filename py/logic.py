from variables import *
from functions import find_signals
import pandas as pd
import numpy as np
import requests
from urllib import urlencode
from datetime import datetime


def run(candle_abv):
    signal_df = pd.DataFrame()
    for ticker in tickers:
        if candle_abv == '1h':
            df = exchange.fetch_ohlcv(ticker, candle_abv, limit=500, since=since)
        else:
            df = exchange.fetch_ohlcv(ticker, candle_abv, limit=500)

        df = pd.DataFrame(df, columns=['date', 'open', 'high', 'low', 'close', 'volume'])

        signals = find_signals(df)
        signals.loc[:, 'ticker'] = ticker
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

    diff = row['price'] - row['stop_loss']
    tp1 = row['price'] + diff/2.
    tp2 = row['price'] + diff
    tp3 = row['price'] + diff*2
    tp4 = row['price'] + diff*3

    if row['ticker'] == 'BTC/USD':
        row['ticker'] = 'XBT/USD'
        row['price'] = int(row['price'])
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
        elif row['ticker'] == 'BCH/BTC':
            decimals = '.5f'
        elif row['ticker'] in ['XRP/USD', 'EOS/USD', 'ETH/BTC']:
            decimals = '.4f'
        else:
            decimals = '.2f'
        row['price'] = format(row['price'], decimals)
        row['stop_loss'] = format(row['stop_loss'], decimals)
        tp1 = format(tp1, decimals)
        tp2 = format(tp2, decimals)
        tp3 = format(tp3, decimals)
        tp4 = format(tp4, decimals)

    if '/BTC' in row['ticker'] and row['ticker'] != 'ETH/BTC':
        row['ticker'] = row['ticker'][:3] + '/U19'

    text = candle_string + '\n'
    text += row['ticker'] + '\n'
    text += 'BitMEX\n'
    text += row['signal'] + ' ' + str(row['price']) + '\n'
    text += 'Take profit ' + str(tp1) + ', ' + str(tp2) + ', ' + str(tp3) + ', ' + str(tp4) + '\n'
    text += 'Leverage ' + leverage +  '\n'
    text += 'Stop loss ' + str(row['stop_loss'])

    if row['ticker'] in ['XBT/USD', 'ETH/USD', 'ETH/BTC']:
        requests.get(url + urlencode({'chat_id': signal_chat_id, 'text': text}))

    requests.get(url + urlencode({'chat_id': test_chat_id, 'text': text}))

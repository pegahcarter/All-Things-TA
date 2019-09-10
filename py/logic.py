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

    if row['ticker'] == 'BTC/USD':
        row['ticker'] = 'XBT/USD'
    elif '/BTC' in row['ticker'] and row['ticker'] != 'ETH/BTC':
        row['ticker'] = row['ticker'][:3] + '/U19'


    if candle_string == 'Hourly':
        leverage = '10x'
    else:   # candle_string == 'Daily'
        leverage = '3x'

    low_price = row['price'] * .999
    high_price = row['price'] * 1.001

    diff = row['price'] - row['stop_loss']
    tp1 = row['price'] + diff/2.
    tp2 = row['price'] + diff
    tp3 = row['price'] + diff*2
    tp4 = row['price'] + diff*3

    if row['ticker'] == 'XBT/USD':
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

    if row['ticker'] in ['XBT/USD', 'ETH/BTC']:
        # ATTA insiders
        # msg_atta(row, tp1, tp2, tp3, tp4)
        # WC elite
        requests.get(url + urlencode({'chat_id': world_class_elite, 'text': text}))
    elif row['ticker'] == ['ETH/USD']:
        # WC4P
        requests.get(url + urlencode({'chat_id': world_class, 'text': text}))
    elif '/USD' not in row['ticker']:
        # WC elite
        requests.get(url + urlencode({'chat_id': world_class_elite, 'text': text}))

    # test bot
    requests.get(url + urlencode({'chat_id': test_chat_id, 'text': text}))


def msg_atta(row, tp1, tp2, tp3, tp4):

    if row['ticker'] == 'ETH/BTC':
        row['ticker'] = 'ETH/U19'
        row['stop_loss'] = int(row['stop_loss'] * 100000)
        tp1 = int(tp1 * 100000)
        tp2 = int(tp2 * 100000)
        tp3 = int(tp3 * 100000)
        tp4 = int(tp4 * 100000)

    low_price = int(row['stop_loss'] * .9982)
    high_price = int(row['stop_loss'] * 1.0018)

    msg = '🚀🚀' + row['ticker'] + '🚀🚀' + '\n\n'
    msg += 'BitMEX' + '\n\n'
    msg += 'Short ' + str(low_price) + ' - ' + str(high_price) + '\n\n'
    msg += 'Sell ' + str(tp1) + ', ' + str(tp2) + ', ' + str(tp3) + ', ' + str(tp4) + '\n\n'
    msg += 'Leverage 5x' + '\n\n'
    msg += 'Stop Loss: ' + str(row['stop_loss'])  + '\n\n'
    msg += '*Disclaimer: Please consult a financial advisor before investing/trading.  This is not financial advice🚀🚀' + '\n\n'
    msg += '💰💰' + '@Allthingstaadmin' + '💰💰'

    # requests.get(url + urlencode({'chat_id': atta_insiders, 'text': msg}))

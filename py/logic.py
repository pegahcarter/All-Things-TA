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
    ticker = row['ticker']
    signal = row['signal']
    price = row['price']
    stop_loss = row['stop_loss']

    if ticker == 'BTC/USD':
        ticker = 'XBT/USD'
    elif '/BTC' in ticker and ticker != 'ETH/BTC':
        ticker = ticker[:3] + '/U19'

    if candle_string == 'Hourly':
        leverage = '10x'
    else:   # candle_string == 'Daily'
        leverage = '3x'

    if ticker == 'XBT/USD':
        decimals = '0.0f'
    elif ticker == 'XRP/U19':
        decimals = '.8f'
    elif ticker == 'EOS/U19':
        decimals = '.7f'
    elif ticker == 'LTC/U19':
        decimals = '.6f'
    elif ticker in ['BCH/U19', 'ETH/BTC']:
        decimals = '.5f'
    elif ticker in ['XRP/USD', 'EOS/USD']:
        decimals = '.4f'
    else:
        decimals = '.2f'

    low_price = price * .999
    high_price = price * 1.001

    low_price = format(low_price, decimals)
    high_price = format(high_price, decimals)

    diff = price - stop_loss

    tp1 = price + diff/2.
    tp2 = price + diff
    tp3 = price + diff*2
    tp4 = price + diff*3

    tp1 = format(tp1, decimals)
    tp2 = format(tp2, decimals)
    tp3 = format(tp3, decimals)
    tp4 = format(tp4, decimals)

    stop_loss = format(stop_loss, decimals)

    msg = '🚨🚨🚨\n\n'
    msg += '{}\nBitMEX\n'.format(ticker)
    msg += '{} zone {}-{}\n'.format(signal, low_price, high_price)
    msg += 'Take profit {}, {}, {}, {}\n'.format(tp1, tp2, tp3, tp4)
    msg += 'Leverage {}\n'.format(leverage)
    msg += 'Stop loss {}\n\n'.format(stop_loss)
    msg += '🚨🚨🚨'

    if row['ticker'] in ['XBT/USD', 'ETH/BTC']:
        # ATTA insiders
        msg_atta(ticker, signal, stop_loss, tp1, tp2, tp3, tp4)
        # WC elite
        requests.get(url + urlencode({'chat_id': world_class_elite, 'text': msg}))
    elif row['ticker'] == 'ETH/USD':
        # WC elite
        requests.get(url + urlencode({'chat_id': world_class_elite, 'text': msg}))
        # WC4P
        requests.get(url + urlencode({'chat_id': world_class, 'text': msg}))
    elif '/USD' not in row['ticker']:
        # WC elite
        requests.get(url + urlencode({'chat_id': world_class_elite, 'text': msg}))

    # test bot
    requests.get(url + urlencode({'chat_id': test_chat_id, 'text': msg}))


def msg_atta(ticker, signal, stop_loss, tp1, tp2, tp3, tp4):

    if ticker == 'ETH/BTC':
        ticker = 'ETH/U19'
        stop_loss *= 100000
        tp1 *= 100000
        tp2 *= 100000
        tp3 *= 100000
        tp4 *= 100000

    low_price = stop_loss * .9982
    high_price = stop_loss * 1.0018

    msg = '🚀🚀{}🚀🚀\n\n'.format(ticker)
    msg += 'BitMEX' + '\n\n'
    msg += '{0:.0f} {0:.0f} - {0:.0f}\n\n'.format(signal, low_price, high_price)
    msg += 'Sell {0:.0f}, {0:.0f}, {0:.0f}, {0:.0f}\n\n'.format(tp1, tp2, tp3, tp4)
    msg += 'Leverage 5x\n\n'
    msg += 'Stop Loss: {0:.0f}\n\n'.format(stop_loss)
    msg += '*Disclaimer: Please consult a financial advisor before investing/trading.  This is not financial advice🚀🚀\n\n'
    msg += '💰💰@Allthingstaadmin💰💰'

    # requests.get(url + urlencode({'chat_id': atta_insiders, 'text': msg}))

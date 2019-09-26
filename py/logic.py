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
        if 'U19' in ticker: ticker = ticker[:3] + '/U19'

        if len(signals) > 0:
            signals.loc[:, 'ticker'] = ticker
            signal_df = signal_df.append(signals, ignore_index=True, sort=False)

    signal_df['date'] = [datetime.fromtimestamp(x/1000) for x in signal_df['date']]
    signal_df = signal_df.sort_values('date').reset_index(drop=True)
    return signal_df



def send_signal(row, candle_string):

    diff = row['price'] - row['stop_loss']

    tp1 = row['price'] + diff/2.
    tp2 = row['price'] + diff
    tp3 = row['price'] + diff*2
    tp4 = row['price'] + diff*3

    msg_wc(row, candle_string, world_class_elite, tp1, tp2, tp3, tp4)
    if row['ticker'] in ['XRP/U19', 'ETH/USD', 'LTC/U19', 'BCH/U19']:
        msg_wc(row, candle_string, world_class, tp1, tp2, tp3, tp4)
    if row['ticker'] in ['BTC/USD', 'ETH/U19']:
        msg_atta(row, tp1, tp2, tp3, tp4)

    # For testing
    # msg_wc(row, candle_string, test_chat_id, tp1, tp2, tp3, tp4)


def msg_wc(row, candle_string, chat_id, *tps):

    if candle_string == 'Hourly':
        leverage = '10x'
    else:   # candle_string == 'Daily'
        leverage = '3x'

    if row['ticker'] == 'BTC/USD':
        decimals = '0.0f'
    elif row['ticker'] == 'XRP/U19' or row['ticker'] == 'ADA/U19':
        decimals = '.8f'
    elif row['ticker'] == 'EOS/U19':
        decimals = '.7f'
    elif row['ticker'] == 'LTC/U19':
        decimals = '.6f'
    elif row['ticker'] in ['BCH/U19', 'ETH/U19']:
        decimals = '.5f'
    else:
        decimals = '.2f'

    low_price, high_price = buy_range(row['price'], .001)

    low_price = format(low_price, decimals)
    high_price = format(high_price, decimals)
    tps = [format(tp, decimals) for tp in tps]
    stop_loss = format(row['stop_loss'], decimals)

    msg = '🚨🚨🚨\n\n'
    msg += '{}\nBitMEX\n'.format(row['ticker'])
    msg += '{} zone {}-{}\n'.format(row['signal'], low_price, high_price)
    msg += 'Take profit {}, {}, {}, {}\n'.format(*tps)
    msg += 'Leverage {}\n'.format(leverage)
    msg += 'Stop loss {}\n\n'.format(stop_loss)
    msg += '🚨🚨🚨'

    requests.get(url + urlencode({'chat_id': chat_id, 'text': msg}))


def msg_atta(row, *tps):
    if row['ticker'] == 'ETH/U19':
        row['price'] *= 100000
        row['stop_loss'] *= 100000
        tps = np.multiply(tps, 100000)

    if row['ticker'] == 'ETH/USD':
        decimals = '.2f'
    else:
        decimals = '0.0f'

    low_price, high_price = buy_range(row['price'], .0018)

    low_price = format(low_price, decimals)
    high_price = format(high_price, decimals)
    tps = [format(tp, decimals) for tp in tps]
    stop_loss = format(row['stop_loss'], decimals)

    msg = '🚀🚀{}🚀🚀\n\n'.format(row['ticker'])
    msg += 'BitMEX' + '\n\n{} '.format(row['signal'])
    msg += '{} - {}\n\n'.format(low_price, high_price)
    msg += 'Sell {}, {}, {}, {}\n\n'.format(*tps)
    msg += 'Leverage 5x\n\n'
    msg += 'Stop Loss: {}\n\n'.format(stop_loss)
    msg += '*Disclaimer: Please consult a financial advisor before investing/trading.  This is not financial advice🚀🚀\n\n'
    msg += '💰💰@Allthingstaadmin💰💰'

    requests.get(url + urlencode({'chat_id': atta_insiders, 'text': msg}))


def buy_range(price, diff):
    low_price = price * (1. - diff)
    high_price = price * (1. + diff)
    return low_price, high_price

from time import mktime
from urllib.parse import urlencode
import requests
from datetime import datetime, timedelta

from functions import *
from variables import *


def run(averages):
    signal_df = pd.DataFrame()
    since = datetime.now() - timedelta(hours=500)

    for ticker in tickers:
        data = exchange.fetch_ohlcv(ticker,
                                    '1h',
                                    limit=500,
                                    since=int(mktime(since.timetuple()) * 1000))

        df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])

        signals = find_signals(df, *averages)
        if 'H20' in ticker: ticker = ticker[:3] + '/H20'

        if len(signals) > 0:
            signals = pd.DataFrame.from_dict(signals).drop('index_opened', axis=1)
            signals.loc[:, 'ticker'] = ticker
            signal_df = signal_df.append(signals, ignore_index=True, sort=False)

    signal_df['date'] = [datetime.fromtimestamp(x/1000) for x in signal_df['date']]

    signal_df = signal_df.sort_values('date').reset_index(drop=True)
    return signal_df


def send_signal(row, channel):

    price = row['price']
    stop_loss = row['stop_loss']
    ticker = row['ticker']
    signal = row['signal']

    if channel == 'wc_elite':
        low_price, high_price = buy_range(price, diff=.00128)
    else:  # channel == 'ata_insiders'
        price *= .9998
        low_price, high_price = buy_range(price, diff=.00111)


    diff = price - stop_loss
    tps = [price + diff/2., price + diff, price + diff*2]

    if ticker == 'ETH/USD':
        low_price = format(low_price, '.2f')
        high_price = format(high_price, '.2f')
        tps = [format(tp, '.2f') for tp in tps]
        stop_loss = format(stop_loss, '.2f')
    elif ticker == 'BTC/USD':
        x = 0
    elif 'BCH' in ticker or 'ETH' in ticker:
        x = 5
    elif 'LTC' in ticker:
        x = 6
    elif 'EOS' in ticker:
        x = 7
    elif 'XRP' in ticker:
        x = 8

    if channel == 'wc_elite':
        if ticker != 'ETH/USD':
            decimals = '.' + str(x) + 'f'
            low_price = format(low_price, decimals)
            high_price = format(high_price, decimals)
            tps = [format(tp, decimals) for tp in tps]
            stop_loss = format(stop_loss, decimals)
        msg_wc(ticker, signal, stop_loss, low_price, high_price, tps)
    else:     # channel == 'atta_insiders'
        if ticker != 'ETH/USD':
            low_price = int(low_price * 10**x)
            high_price = int(high_price * 10**x)
            tps = [int(tp * 10**x) for tp in tps]
            stop_loss = int(stop_loss * 10**x)
        msg_atta(ticker, signal, stop_loss, low_price, high_price, tps)


def buy_range(price, diff=0):
    low_price = price * (1. - diff)
    high_price = price * (1. + diff)
    return low_price, high_price


def msg_wc(ticker, signal, stop_loss, low_price, high_price, tps):

    text = '🚨🚨🚨\n\n'
    text += '{}\nBitMEX\n'.format(ticker)
    text += '{} zone {}-{}\n'.format(signal, low_price, high_price)
    text += 'Take profit {}, {}, {}\n'.format(*tps)
    text += 'Leverage 10x\n'
    text += 'Stop loss {}\n\n'.format(stop_loss)
    text += '🚨🚨🚨'

    # requests.get(url + urlencode({'chat_id': '@testgbot123', 'text': text}))
    requests.get(url + urlencode({'chat_id': wc_id, 'text': text}))

    # if ticker in ['XRP/H20', 'LTC/H20', 'BCH/H20']:
    requests.get(url + urlencode({'chat_id': wc_elite_id, 'text': text}))



def msg_atta(ticker, signal, stop_loss, low_price, high_price, tps):

    text = '🚀🚀{}🚀🚀\n\n'.format(ticker)
    text += 'BitMEX' + '\n\n{} '.format(signal)
    text += '{} - {}\n\n'.format(low_price, high_price)
    text += 'Sell {}, {}\n\n'.format(tps[0], tps[1])
    text += 'Leverage 5x\n\n'
    text += 'Stop Loss: {}\n\n'.format(stop_loss)
    text += '*Disclaimer: Please consult a financial advisor before investing/trading.  This is not financial advice🚀🚀\n\n'
    text += '💰💰@Allthingstaadmin💰💰'

    # requests.get(url + urlencode({'chat_id': '@testgbot123', 'text': text}))
    requests.get(url + urlencode({'chat_id': atta_id, 'text': text}))

    # if ticker in ['BTC/USD', 'ETH/USD',  'ETH/H20']:
    requests.get(url + urlencode({'chat_id': atta_insiders_id, 'text': text}))

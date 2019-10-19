from functions import *


def run(channel):
    signal_df = pd.DataFrame()
    since = datetime.now() - timedelta(hours=500)

    for ticker in tickers:
        data = exchange.fetch_ohlcv(ticker,
                                    '1h',
                                    limit=500,
                                    since=int(time.mktime(since.timetuple()) * 1000))

        df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])

        signals = find_signals(df, *channel['averages'])
        if 'Z19' in ticker: ticker = ticker[:3] + '/Z19'

        if len(signals) > 0:
            signals.loc[:, 'ticker'] = ticker
            signal_df = signal_df.append(signals, ignore_index=True, sort=False)

    signal_df['date'] = [datetime.fromtimestamp(x/1000) for x in signal_df['date']]
    signal_df = signal_df.sort_values('date').reset_index(drop=True)
    return signal_df



def send_signal(row, channel):

    diff = row['price'] - row['stop_loss']

    tp1 = row['price'] + diff/2.
    tp2 = row['price'] + diff
    tp3 = row['price'] + diff*2
    tp4 = row['price'] + diff*3

    if channel['name'] == 'world_class_elite':
        msg_wc(row, tp1, tp2, tp3, tp4)
    else:     # channel['name'] == 'atta_insiders'
        msg_atta(row, tp1, tp2, tp3, tp4)

    # For testing
    # msg_wc(row, test_chat_id, tp1, tp2, tp3, tp4)


def msg_wc(row, *tps):

    if row['ticker'] == 'BTC/USD':
        decimals = '0.0f'
    elif row['ticker'] == 'XRP/Z19':
        decimals = '.8f'
    elif row['ticker'] == 'EOS/Z19':
        decimals = '.7f'
    elif row['ticker'] == 'LTC/Z19':
        decimals = '.6f'
    elif row['ticker'] in ['BCH/Z19', 'ETH/Z19']:
        decimals = '.5f'
    else:  # row['ticker'] == 'ETH/USD'
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
    msg += 'Leverage 10x\n'
    msg += 'Stop loss {}\n\n'.format(stop_loss)
    msg += '🚨🚨🚨'

    requests.get(url + urlencode({'chat_id': channel['chat_id'], 'text': msg}))

    if row['ticker'] in ['XRP/Z19', 'ETH/USD', 'LTC/Z19', 'BCH/Z19']:
        requests.get(url + urlencode({'chat_id': '@worldclasstrader', 'text': msg}))



def msg_atta(row, *tps):

    elif row['ticker'] == 'XRP/Z19':
        multiplier = 10**8
    elif row['ticker'] == 'EOS/Z19':
        multiplier = 10**7
    elif row['ticker'] == 'LTC/Z19':
        multiplier = 10**6
    elif row['ticker'] in ['BCH/Z19', 'ETH/Z19']:
        multiplier = 10**5

    if row['ticker'] == 'ETH/Z19':
        row['price'] *= 100000
        row['stop_loss'] *= 100000
        tps = np.multiply(tps, 100000)

    if row['ticker'] == 'ETH/USD':
        decimals = '.2f'
    else:
        decimals = '0.0f'
        row['price'] *= multiplier
        row['stop_loss'] *= multiplier
        tps = np.multiply(tps, multiplier)

    low_price, high_price = buy_range(row['price'], .001)

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

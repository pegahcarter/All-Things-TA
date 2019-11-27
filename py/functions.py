from utils import *


def find_signals(df, window_fast, window_mid, window_slow):
    ''' Determine signals from OHLCV dataframe '''

    emaslow = ema(df['close'], span=window_slow)
    mamid = sma(df['close'], window=window_mid)
    emafast = ema(df['close'], span=window_fast)
    mabase = sma(df['close'], window=200)

    mamid_emaslow_diff = abs(mamid - emaslow) / mamid

    candle_body = abs(df['close'] - df['open']) / df['open']
    candle_std = candle_body.rolling(168).std().tolist()
    candle_body = candle_body.tolist()
    relative_strength = rsi(df['close'])

    close = df['close'].tolist()
    high = df['high'].tolist()
    low = df['low'].tolist()

    signals = {}

    for i in crossover(emafast, mamid):
        if i < 48:
            continue

        body_sorted = sorted(candle_body[i-48:i], reverse=True)
        window_std = np.mean(candle_std[i-48:i])
        candle_mean = np.median(candle_body[i-48:i])

        if (high[i] - low[i]) / high[i] > 0.02 \
        or max(candle_body[i-24:i]) > .025 \
        or sum(body_sorted[:3]) - (4*candle_mean) > 12*window_std:
            continue

        price = close[i]
        signal = None

        if price > emafast[i]:
            if mamid[i] > emaslow[i] and relative_strength[i] > 50 and price > mabase[i]:
                signal = 'long'
                stop_loss = min(low[i-10:i])
        else:   # price < emafast[i]
            if mamid[i] < emaslow[i] and relative_strength[i] < 50 and price < mabase[i]:
                signal = 'short'
                stop_loss = max(high[i-10:i])

        if signal and 0.0075 < abs(1 - stop_loss/price) < .04 and mamid_emaslow_diff[i] > .001:
            signals[i] = {'date': df['date'][i],
                          'signal': signal,
                          'price': price,
                          'stop_loss': stop_loss}

    return pd.DataFrame.from_dict(signals, orient='index')


def determine_TP(df, signals, cushion=0):
    ''' Figure out which TP level is hit '''

    tp_lst = []
    index_tp_hit_lst = []

    low = df['low'].tolist()
    low_inverse = (-df['low']).tolist()
    high = df['high'].tolist()
    high_inverse = (-df['high']).tolist()

    for index, row in signals.iterrows():
        price = row['price']
        stop_loss = row['stop_loss']
        if row['signal'] == 'long':
            l_bounds = low
            u_bounds = high
        else:   # signal == 'short'
            l_bounds = high_inverse
            u_bounds = low_inverse
            cushion *= -1
            price *= -1
            stop_loss *= -1

        diff = price - stop_loss
        # stop_loss *= (1. + cushion)

        tp1 = price + diff/2.
        tp2 = price + diff
        tp3 = price + diff*2
        tp4 = price + diff*3

        tp_targets = [tp1, tp2, tp3, tp4]
        index_tp_hit = [0, 0, 0, 0]
        tp = 0

        for x in range(index+1, len(df)):
            while tp != 4 and u_bounds[x] > tp_targets[tp]:
                index_tp_hit[tp] = x
                tp += 1
            if tp == 4 or l_bounds[x] < stop_loss:
                break
            if tp > 0:
                stop_loss = price

        tp_lst.append(tp)
        index_tp_hit_lst.append(index_tp_hit)

    return tp_lst, index_tp_hit_lst



# ------------------------------------------------------------------------------
# Old functions

def find_intersections(line1, line2):
    ''' Find intersections indices between two lines '''

    line1_gt_line2 = line1 > line2
    intersections = []
    current_val = line1_gt_line2[0]

    for i, val in line1_gt_line2.items():
        if val != current_val:
            intersections.append(i)
        current_val = val

    return intersections


def net_profit_pct(tp_pcts, tps_hit, prices, stop_losses):
    ''' Return outcome of TP in % '''

    profit_pct = abs(prices - stop_losses) / prices
    end_pct = list(map(lambda x: tp_pcts[x], tps_hit))
    return profit_pct * end_pct


def drop_extra_signals(signals, gap=0):
    ''' TODO: conceptually this is very similar to find_intersections().  Is
    there a reasonable way to combine them into one function? '''

    last_signal = 0
    clean_signals = []
    for signal in signals.index:
        if signal > last_signal + gap:
            clean_signals.append(signal)
        last_signal = signal
    return signals.drop([i for i in signals.index if i not in clean_signals])


def refresh_ohlcv(file, offline=False):
    ''' Loop to update CSVs with recent OHLCV data '''

    df = pd.read_csv('prices/' + file)
    if 'signal' in df.columns:
        df.drop('signal', axis=1,inplace=True)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')
    coin = file[:file.find('.')]

    if offline:
        return coin, df

    start_date = df.iloc[-1]['date']
    df_new = []
    binance = ccxt.binance()

    while start_date < datetime.now():
        results = binance.fetch_ohlcv(coin + '/USDT', '1h', since=int(start_date.timestamp()*1000))
        df_new += results
        start_date += timedelta(hours=len(results))

    df_new = pd.DataFrame(df_new, columns=df.columns)
    df_new['date'] = df_new['date'].apply(lambda x: datetime.fromtimestamp(x/1000))
    df_new = df_new[df_new['date'] > df.iloc[-1]['date']]
    df = df.append(df_new, ignore_index=True)
    df.to_csv('prices/' + file, index=False)

    return coin, df

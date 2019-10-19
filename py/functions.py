from utils import *


# Determine signals from OHLCV dataframe
def find_signals(df, window_fast, window_mid, window_slow):

    emaslow = ema(df['close'], span=window_slow)
    mamid = df['close'].rolling(window=window_mid).mean().fillna(0)
    emafast = ema(df['close'], span=window_fast)

    mamid_emaslow_diff = abs(mamid - emaslow) / mamid

    candle_body = abs(df['close'] - df['open']) / df['open']
    candle_std = candle_body.rolling(168).std()
    relative_strength = rsi(df['close'])

    intersections = crossover(emafast, mamid)
    signals = {}

    for i in intersections:
        if i < 48:
            continue

        signal = None
        price = df['close'][i]
        high = df['high'][i]
        low = df['low'][i]

        body_sorted = sorted(candle_body[i-48:i], reverse=True)
        window_std = candle_std[i-48:i].mean()
        candle_mean = candle_body[i-48:i].median()

        if sum(body_sorted[:3]) - (4*candle_mean) > 12*window_std \
        or candle_body[i-24:i].max() > .025 \
        or (high - low) / high > 0.02:
            continue

        if price > emafast[i]:
            if mamid[i] > emaslow[i] and relative_strength[i] > 50:
                signal = 'Long'
                stop_loss = df['low'][i-10:i].min()
        else:   # price < emafast[i]
            if mamid[i] < emaslow[i] and relative_strength[i] < 50:
                signal = 'Short'
                stop_loss = df['high'][i-10:i].max()

        if signal and 0.0075 < abs(1 - stop_loss/price) < .04 and mamid_emaslow_diff[i] > .001:
            signals[i] = {'date': df['date'][i],
                          'signal': signal,
                          'price': price,
                          'stop_loss': stop_loss}

    signals = pd.DataFrame.from_dict(signals, orient='index')
    return signals


# Figure out which TP level is hit
def determine_TP(df, signals, cushion=0, compound=False):
    tp_lst = []
    index_closed_lst = []
    index_tp_hit_lst = []

    for index, row in signals.iterrows():
        if row['signal'] == 'Long':
            l_bounds = df['low']
            u_bounds = df['high']
        else:   # signal == 'Short'
            l_bounds = -df['high']
            u_bounds = -df['low']
            cushion *= -1
            row['price'] *= -1
            row['stop_loss'] *= -1

        row['stop_loss'] *= (1. + cushion)
        if row['stop_loss'] > row['price']:
            tp_lst.append(5)
            index_closed_lst.append(index)
        else:
            diff = row['price'] - row['stop_loss']

            tp1 = row['price'] + diff/2.
            tp2 = row['price'] + diff
            tp3 = row['price'] + diff*2
            tp4 = row['price'] + diff*3

            tp_targets = [tp1, tp2, tp3, tp4]
            index_tp_hit = [0, 0, 0, 0]
            tp = 0

            for x in range(index+1, len(df)):
                while tp != 4 and u_bounds[x] > tp_targets[tp]:
                    index_tp_hit[tp] = x
                    tp += 1
                if tp == 4 or l_bounds[x] < row['stop_loss']:
                    break
                if tp > 0:
                    row['stop_loss'] = row['price']

            tp_lst.append(tp)
            index_closed_lst.append(x)
            index_tp_hit_lst.append(index_tp_hit)

    if compound:
        return tp_lst, index_closed_lst, index_tp_hit_lst
    else:
        return tp_lst


# ------------------------------------------------------------------------------
# Old functions

# Find intersections indices between two lines
def find_intersections(line1, line2):
    line1_gt_line2 = line1 > line2
    intersections = []
    current_val = line1_gt_line2[0]

    for i, val in line1_gt_line2.items():
        if val != current_val:
            intersections.append(i)
        current_val = val

    return intersections


# Return outcome of TP in %
def net_profit_pct(tp_pcts, tps_hit, prices, stop_losses):
    profit_pct = abs(prices - stop_losses) / prices
    end_pct = list(map(lambda x: tp_pcts[x], tps_hit))
    return profit_pct * end_pct


# TODO: conceptually this is very similar to find_intersections().  Is there a
# reasonable way to combine them into one function?
def drop_extra_signals(signals, gap=0):
    last_signal = 0
    clean_signals = []
    for signal in signals.index:
        if signal > last_signal + gap:
            clean_signals.append(signal)
        last_signal = signal
    return signals.drop([i for i in signals.index if i not in clean_signals])


# Loop to update CSV's with recent OHLCV data
def refresh_ohlcv(file, offline=False):

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

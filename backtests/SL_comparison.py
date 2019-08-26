# Determine the best SL and TP levels for 3EMA, 20MA, and 40EMA
import pandas as pd
from py.functions import find_signals, determine_TP, drop_extra_signals

df = pd.read_csv('backtests/BTC.csv')
signals = find_signals(df)
signals['profit_pct'] = abs(signals['price'] - signals['stop_loss']) / signals['price']
# signals['stop_loss'] = (signals['stop_loss'] + signals['price']) / 2.

signals[0] = determine_TP(df, signals)
signals = signals.sort_values('profit_pct')

tp_pcts = [-1, 0.125, 0.375, 0.875, 1.375]
signals['end_pct'] = list(map(lambda x: tp_pcts[x], signals[0]))
signals['net_profit'] = signals['end_pct'] * signals['profit_pct']
signals['net_profit'].sum()

signals.groupby(0).count()





for cushion in range(15, 100, 5):
    cushion /= 10000
    signals[cushion] = determine_TP(df, cushion)









df = pd.DataFrame()
# Now that we have our signals, test out the different SL & TP levels
# By increments of .05%, find the SL that returns the most profit
for multiplier in range(15, 100, 5):
    multiplier /= 10000.
    profit_pct_list = []
    for index in signals:
        if signals[index] == 'Long':
            l_bounds = _low
            midrange = _open
            u_bounds = _high
            cushion = 1. + multiplier
        else:  # Signal == 'Short'
            l_bounds = -_high
            midrange = -_open
            u_bounds = -_low
            cushion = 1. - multiplier

        purchase_price = midrange[index+1]
        stop_loss = min(l_bounds[index-10:index]) * cushion

        diff = abs(purchase_price) - abs(stop_loss)
        stop_loss_pct = abs(1 - stop_loss/purchase_price)

        tp1 = purchase_price + diff/2.
        tp2 = purchase_price + diff
        tp3 = purchase_price + diff*2
        tp4 = purchase_price + diff*3
        tp_targets = [tp1, tp2, tp3, tp4]

        if stop_loss > tp1:
            profit_pct = None
        else:
            tp = 0
            for x in range(index, len(_open)):
                if tp == 4 or l_bounds[x] < stop_loss:
                    break
                if tp > 0:
                    stop_loss = purchase_price
                while tp < 4 and u_bounds[x] > tp_targets[tp]:
                    tp += 1

            profit_pct = stop_loss_pct * tp_pcts[tp]

        profit_pct_list.append(profit_pct)
    df[multiplier] = profit_pct_list


results = {}
for col in df.columns:
    results[col] = round(df[col].dropna().sum(), 4)

results

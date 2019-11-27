from py.functions import *

'''
TP1
Sell 10% at TP1, 90% @ breakeven

TP2
Sell 10% at TP1, 10% @ TP2, 80% @ breakeven

TP3
Sell 10% at TP1, 10% @ TP2, 10% @ TP3, 70% @ breakeven

TP4
Sell 10% at TP1, 10% @ TP2, 10% @ TP3, 70% @ TP4

# Let's assume fee is .075%
'''

tp_pcts = [-1, .05, .15, .35, 2.45]
tp_pct_absolute = [-1, .05, .1, .2, 2.1]

df = pd.read_csv('data/bitfinex/BTC.csv')

signals = find_signals(df)
tp, index_closed, index_tp_hit = determine_TP(df, signals, compound=True)

signals['tp'] = tp
signals['index_closed'] = index_closed
signals['index_tp_hit'] = index_tp_hit
signals['index_opened'] = signals.index
signals = signals.reset_index(drop=True)

potential_profit = abs(signals['price'] - signals['stop_loss']) / signals['price']
signals['potential_profit'] = potential_profit
end_pct = signals['tp'].apply(lambda x: tp_pcts[x])
signals['net_profit'] = potential_profit * end_pct

# ------------------------------------------------------------------------------
# NOTE: this is based on market orders.

potential_profit = .02
normal_fee = .0075

# SL
normal_fee * (1 + tp_pcts[0] * potential_profit)

# TP1
normal_fee * (1 + tp_pcts[1] * potential_profit)
# TP2
normal_fee * (1 + tp_pcts[2] * potential_profit)
# TP3
normal_fee * (1 + tp_pcts[3] * potential_profit)
# TP4
normal_fee * (1 + tp_pcts[4] * potential_profit)



# ------------------------------------------------------------------------------
# Old calculations that assumed we pay a funding fee per hour
units_borrowed = []
for _, row in signals.iterrows():
    open_to_close = [row['index_opened']] + row['index_tp_hit'][:row['tp']]
    if row['tp'] != 4:
        open_to_close += [row['index_closed']]

    hrs_between_tp = np.diff(open_to_close)
    units = np.dot(hrs_between_tp, pct_holding[:row['tp']+1])
    units_borrowed.append(units)

units_borrowed

# # Testing for calculations with TP4
# signals.iloc[15:16]
#
# test_tp = tp[15]
# test_index_open = signals.iloc[15].name
# test_index_closed = index_closed[15]
# test_index_tp_hit = index_tp_hit[15]
#
# pcts = [.1, .1, .1, .7]
#
# open_to_close = [test_index_open] + test_index_tp_hit
# hrs_between_tp = np.diff(open_to_close)
#
# pct_before_tp1 = 1
# pct_after_tp1 = pct_before_tp1 - pcts[0]
# pct_after_tp2 = pct_after_tp1 - pcts[1]
# pct_after_tp3 = round(pct_after_tp2 - pcts[2], 1)
# pct_holding = [pct_before_tp1, pct_after_tp1, pct_after_tp2, pct_after_tp3]
#
# np.dot(pct_holding, hrs_between_tp)
# np.dot(hrs_between_tp, pct_holding[:test_tp+1])
#
#
# # Testing calculations for TP0
# test_tp = tp[0]
# test_index_open = signals.iloc[0].name
# test_index_closed = index_closed[0]
# test_index_tp_hit = index_tp_hit[0]
#
# open_to_close = [test_index_open] + test_index_tp_hit[:0] + [test_index_closed]
# hrs_between_tp = np.diff(open_to_close)
#
# hrs_between_tp[0] * pct_holding[0]
# np.dot(hrs_between_tp, pct_holding[:test_tp + 1])
#
# # np.count_nonzero(x)
# # Testing calculations for TP1-TP3
# test_tp = tp[6]
# test_index_open = signals.iloc[6].name
# test_index_closed = index_closed[6]
# test_index_tp_hit = index_tp_hit[6]
#
# test_index_tp_hit[3]
#
# open_ = [test_index_open] + test_index_tp_hit[:3]
# open_ = [test_index_open] + test_index_tp_hit[:3] + [test_index_closed]
# hrs_between_tp = np.diff(open_)
# np.dot(hrs_between_tp, pct_holding)
# Math for TP targets
(9800 - 10000) * 1
(10100 - 10000)*.25 + (9800 - 10000)*.75
(10100 - 10000)*.25 + (10200 - 10000)*.25
(10100 - 10000)*.25 + (10200 - 10000)*.25 + (10400 - 10000)*.25
(10100 - 10000)*.25 + (10200 - 10000)*.25 + (10400 - 10000)*.25  + (10600 - 10000)*.25


# # Testing for single signal
buy = df.iloc[13165]
SL = df[13155:13165]['low'].min() * .9975
purchase_price = buy['open']
diff = purchase_price - SL
diff_pct = diff / purchase_price

tp1 = purchase_price + diff/2
tp2 = purchase_price + diff
tp3 = purchase_price + diff*2
tp4 = purchase_price + diff*3

tp_targets = iter([tp1, tp2, tp3, tp4])
tp_target = next(tp_targets, None)
result = 0

for i, row in df[13165:].iterrows():

    if row['open'] < SL or row['low'] < SL or result == 4:
        break

    while result != 4 and row['high'] > tp_target:
        result += 1
        tp_target = next(tp_targets, None)

    if result == 2:
        SL = purchase_price

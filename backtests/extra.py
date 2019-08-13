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



# Comparing performance of different candle periods to the hourly period
windows = [4, 6, 12, 24, 36]

def correct(window, row):
    if row['signal'] == 'BUY':
        if row['close_' + str(window)] > row['close']:
            return True
        else:
            return False
    else:  # row['signal'] == 'SELL'
        if row['close_' + str(window)] < row['close']:
            return True
        else:
            return False



coin = 'BTC'
df_all = pd.read_csv('prices/' + coin + '.csv')

df = df_all.dropna().copy()
results = pd.DataFrame()

for window in windows:
    df['close_' + str(window)] = [group_candles(df_all[i:i+window])[4] for i in df.index]
    df['close_'+str(window)+'_delta'] = [(row['close_'+str(window)] - row['close']) / row['close'] for _, row in df.iterrows()]
    results[window] = [correct(window, row) for _, row in df.iterrows()]


df.drop(['open', 'high', 'low', 'volume'], axis=1, inplace=True)

cols = [col for col in df.columns if 'delta' in col]

df.groupby('signal')[cols].mean()

df.head(20)

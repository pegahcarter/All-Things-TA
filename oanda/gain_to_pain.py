# Pain to gain ratio
df = all_signals(0.0075, 0.04)

df['profit'] = [df['pct'][i] * tps[df['tp'][i]] for i in range(len(df))]
df[df['tp'] == 0]['profit'].sum()
df[df['tp'] != 0]['profit'].sum()

5.22 / 2.49  # 2.09

df = all_signals(0, 1)


df['profit'] = [df['pct'][i] * tps[df['tp'][i]] for i in range(len(df))]
df[df['tp'] == 0]['profit'].sum()
df[df['tp'] != 0]['profit'].sum()

5.89 / 3.26

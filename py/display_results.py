import os
import pandas as pd

df = pd.DataFrame(columns=['coin','date','signal'])

for file in os.listdir('prices/'):
    df_coin = pd.read_csv('prices/' + file).dropna()
    coin = file[:file.find('.')]
    df_coin['coin'] = coin
    df = df.append(df_coin[['coin', 'date', 'signal']], ignore_index=True)


df.to_csv('signals.csv', index=True)

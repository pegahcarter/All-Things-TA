import os
import pandas as pd
import logic as logic
from variables import *
from datetime import datetime
from urllib.parse import urlencode
import requests
import time


for candle_abv, candle_string in candle_intervals.items():
    text = candle_string + '\n'
    signal_df = []
    for ticker in tickers:
        signal_df += logic.run(ticker, candle_abv)

    signal_df = pd.DataFrame(signal_df, columns=['date', 'signal', 'coin', 'price'])
    signal_df['date'] = [datetime.fromtimestamp(x/1000) for x in signal_df['date']]
    signal_df = signal_df.sort_values('date').reset_index(drop=True)

    # old_signal_df = pd.read_csv('C:/Users/carter/Documents/crypto/peter-signal/signals/' + candle_string + '.csv')
    old_signal_df = get_gsheet(candle_string)
    new_signals = signal_df.loc[signal_df['date'] > old_signal_df['date'].iloc[-1]]

    if len(new_signals) > 0:
        for _, row in new_signals.iterrows():
            if candle_string == 'Hourly':
                date = row['date'].strftime('%m/%d %I:%M %p')
            else:  # candle_string == 'Daily'
                date = row['date'].strftime('%m/%d')

            text += date + ': ' + row['coin'] + ' - ' + row['signal'] + ' - '  + str(round(row['price'], 8)) +  '\n\n'

        old_signal_df = old_signal_df.append(signal_df, ignore_index=True, sort=False)
        # old_signal_df.to_csv('C:/Users/carter/Documents/crypto/peter-signal/signals/' + candle_string + '.csv', index=False)
        save_gsheet(candle_string, old_signal_df)

        requests.get(url + urlencode({'chat_id': chat_id, 'text': text}))

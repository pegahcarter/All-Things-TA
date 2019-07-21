import os
import pandas as pd
import py.logic as logic
from py.variables import *
from datetime import datetime
from urllib import quote_plus
import requests

def main():

    signal_df = []
    for ticker in tickers:
        data = bitmex.fetch_ohlcv(ticker, '1h', limit=500, since=since)
        df = pd.DataFrame(data=data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        df['date'] = [datetime.fromtimestamp(x/1000) for x in df['date']]

        coin_signals = logic.run(ticker, df)
        signal_df += coin_signals

    signal_df = pd.DataFrame(signal_df, columns=['date', 'signal', 'coin', 'price'])
    signal_df = signal_df.sort_values('date').reset_index(drop=True)

    old_signal_df = pd.read_csv('signals.csv')
    new_signals = signal_df.loc[signal_df['date'] > old_signal_df['date'].iloc[-1]]

    message = ''
    if len(new_signals) > 0:
        for _, row in new_signals.iterrows():
            date = row['date'].strftime('%m/%d %H:%M %p (CST)')
            message += date + '  -  ' + row['coin'] + '  -  ' + row['signal'] + '  -  '  + str(row['price']) +  '\n\n'

        old_signal_df = old_signal_df.append(signal_df, ignore_index=True, sort=False)
        old_signal_df.to_csv('signals.csv', index=False)
        message = 'https://api.telegram.org/bot' + API_KEY + '/sendMessage?chat_id=' + CHAT_ID + '&text=' + quote_plus(message)
        requests.get(message)


if __name__ == '__name__':
    main()

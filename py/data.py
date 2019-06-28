from datetime import datetime, timedelta
from time import sleep
import pandas as pd
import ccxt
import os



def main():

    for file in os.listdir('data/'):
        df = pd.read_csv('data/' + file)
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')

        binance = ccxt.binance()
        coin = file[:file.find('.')]

        df_new = []
        start_date = df.iloc[-1]['date']
        while start_date < datetime.now():
            results = binance.fetch_ohlcv(coin + '/USDT', '1h', since=int(start_date.timestamp()*1000))
            df_new += results
            start_date += timedelta(hours=len(results))
            sleep(1)

        df_new = pd.DataFrame(df_new, columns=df.columns)
        df_new['date'] = df_new['date'].apply(lambda x: datetime.fromtimestamp(x/1000))
        df_new = df_new[df_new['date'] > df.iloc[-1]['date']]

        df = df.append(df_new, ignore_index=True)
        df.to_csv('data/' + file, index=False)


if __name__ == '__main__':
    main()

import os
import ccxt
import pandas as pd
import py.logic as logic
from py.variables import *
from datetime import datetime, timedelta
from time import sleep


def main():

    data = binance.fetch_ohlcv(coin + '/USDT', '4h', limit=500)
    df = pd.DataFrame(data=data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])

    message = ''
    for coin in coins:

    logic.run(df)


    last_candle = df.iloc[-1]

    if last_candle['signal'] is not None:
        message += coin + ' - ' + candle['signal'] + '\n'
        message += candle['date'].strftime('%H:%M %p %B %d') + '\n\n'



if __name__ == '__name__':
    main()

import os
import ccxt
import pandas as pd
import py.logic as logic
from py.variables import *
from datetime import datetime, timedelta
from time import sleep
from twilio.rest import Client


def main():
    binance = ccxt.binance()
    client = Client(account_sid, auth_token)
    while True:
        sleep(45)
        if datetime.now().minute == 1:
            sleep(60)
            message = ''
            for coin in coins:
                data = binance.fetch_ohlcv(coin + '/USDT', '4h', limit=500)
                df = pd.DataFrame(data=data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
                logic.run(df)
                last_candle = df.iloc[-1]
                if last_candle['signal'] is not None:
                    message += coin + ' - ' + candle['signal'] + '\n'
                    message += candle['date'].strftime('%H:%M %p %B %d') + '\n\n'
            if len(message) > 0:
                client.messages.create(
                    from_=twilio_number,
                    body=message,
                    to=recipient
                )



if __name__ == '__name__':
    main()

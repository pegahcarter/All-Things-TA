import ccxt
import pandas as pd
from datetime import datetime, timedelta
from time import sleep

df = pd.read_csv('prices/BTC.csv')
df = df.dropna().reset_index(drop=True)

test = df[-1:].values[0]
# Remove milliseconds from date
test[0] = test[0][:-4]

last_date = datetime.strptime(test[0], '%Y-%m-%d %H:%M:%S')

'BTC - ' + test[-1]
last_date = last_date.strftime('%H:%M %p %B %d ')


# -----------------------------------------------------------------------
# Initial psuedocode

b = ccxt.binance()
data = b.fetch_ohlcv('BTC/USDT', '1h', limit=500)

last_candle = data[-1]
datetime.fromtimestamp(last_candle[0]/1000)


coins = ['BTC', 'ETH', 'LTC', 'BCH', 'BNB']
b = ccxt.binance()

while True:
    next_hour = (datetime.now() + timedelta(hours=1)).hour

    while datetime.now().hour < next_hour:
        sleep(60)
        for coin in coins:
            df = b.fetch_ohlcv(coin + '/USDT', '1h', limit=500)

            signals = main_logic()
            # TODO: remove milliseconds?
            last_signal = get_last_signal(signals)
            if last_signal['date'].hour == next_hour:
                send_alert(coin, last_signal)

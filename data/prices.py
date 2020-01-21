# Generic file to find hourly prices for different tickers on Binance
import pandas as pd
import numpy as np
import ccxt
from datetime import datetime, timedelta
import time



for ticker in ['BTC/USDT', 'ETH/BTC', 'ETH/USDT', 'EOS/BTC', 'LTC/BTC', 'XRP/BTC', 'ADA/BTC']:

    start_date = datetime(year=2019, month=1, day=1, hour=1)
    end_date = datetime(year=2020, month=1, day=1, hour=1)
    df = []

    while start_date < end_date:
        data = binance.fetch_ohlcv(ticker, '1h', limit=500, since=int(time.mktime(start_date.timetuple())*1000))
        df.extend(data)

        # Use last date from results to fetch new set of prices
        data = np.array(data)
        last_date = datetime.fromtimestamp(data[-1, 0]/1000)

        # Update start date
        start_date = last_date + timedelta(hours=1)

        # Pause in case we start hitting some API request limits
        time.sleep(.1)

    # Convert list to DataFrame
    df = pd.DataFrame(df, columns=['date', 'open', 'high', 'low', 'close', 'volume'])

    # Convert `date` type from int to datetime
    df['date'] = df['date'].apply(lambda x: datetime.fromtimestamp(x/1000))

    # Save DataFrame
    df.to_csv(f'{ticker.replace("/", "-")}.csv', index=False)

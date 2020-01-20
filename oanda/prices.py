# Pulls 5,000 most recent prices for a ticker
import time
from datetime import datetime, timedelta
import pandas as pd
import oandapyV20
from oandapyV20.endpoints.instruments import InstrumentsCandles
import auth as auth


def prices(ticker):

    _, access_token = auth.Auth()
    client = oandapyV20.API(access_token=access_token)

    start_date = datetime.utcnow() - timedelta(hours=1000)
    start_date_str = datetime.strftime(start_date, '%Y-%m-%dT%H:%M:00Z')
    params = {"from": start_date_str,
              "granularity": 'H1',
              "count": 1000}

    r = InstrumentsCandles(instrument=ticker, params=params)
    response = client.request(r)['candles']

    dates = pd.to_datetime(list(map(lambda x: x['time'], response)))
    candles = list(map(lambda x: list(x['mid'].values()), response))
    volume = list(map(lambda x: x['volume'], response))

    _prices = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    _prices['date'] = dates
    _prices[['open', 'high', 'low', 'close']] = candles
    _prices[['open', 'high', 'low', 'close']] = _prices[['open', 'high', 'low', 'close']].astype(float)
    _prices['volume'] = volume

    return _prices


prices('NAS100_USD')

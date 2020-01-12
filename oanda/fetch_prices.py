# Pulls 5,000 most recent prices for a ticker
import time
from datetime import datetime, timedelta
import pandas as pd
import oandapyV20
from oandapyV20.endpoints.instruments import InstrumentsCandles
import auth as auth


def fetch_prices(ticker, **params):

    if 'backtest' in params:
        prices = pd.read_csv('oanda/data/M5/' + ticker + '.csv')
        prices['date'] = pd.to_datetime(prices['date'])
        return prices

    _, access_token = auth.Auth()
    client = oandapyV20.API(access_token=access_token)

    if 'granularity' not in params:
        params['granularity'] = 'M5'
    if 'count' not in params:
        params['count'] = 5000
    if 'from' not in params:
        params['from'] = datetime.utcnow() - timedelta(minutes=5*params['count'])

    params['from'] = datetime.strftime(params['from'], '%Y-%m-%dT%H:%M:00Z')

    r = InstrumentsCandles(instrument=ticker, params=params)
    response = client.request(r)['candles']

    dates = pd.to_datetime(list(map(lambda x: x['time'], response)))
    candles = list(map(lambda x: list(x['mid'].values()), response))
    volume = list(map(lambda x: x['volume'], response))

    prices = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    prices['date'] = dates
    prices[['open', 'high', 'low', 'close']] = candles
    prices[['open', 'high', 'low', 'close']] = prices[['open', 'high', 'low', 'close']].astype(float)
    prices['volume'] = volume

    return prices

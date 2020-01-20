# This beast of a file creates all files within data/oanda/*

import time
from datetime import datetime, timedelta
import pandas as pd
import oandapyV20
import oandapyV20.endpoints.instruments as instruments
from auth import auth

accountID, access_token = auth.Auth()
client = oandapyV20.API(access_token=access_token)

kwargs = [{'granularity': 'H1', 'hours': 1}, {'granularity': 'M5', 'minutes': 5}]
currencies = ['NAS100_USD', 'US30_USD', 'AUD_USD', 'EUR_USD', 'GBP_USD', 'USD_CAD', 'USD_CHF', 'USD_JPY', 'USD_MXN', 'USD_TRY']

kwarg = kwargs[0]
for kwarg in kwargs:
    granularity = kwarg.pop('granularity')
    print(granularity)
    for currency in currencies:
        dates = []
        candles = []
        volume = []
        params = {"from": "2006-01-01T00:00:00Z",
                  "granularity": granularity,
                  "count": 5000}

        while params['count'] == 5000:
            try:
                r = instruments.InstrumentsCandles(instrument=currency, params=params)
                response = client.request(r)['candles']
            except:
                break

            response_dates = pd.to_datetime(list(map(lambda x: x['time'], response)))
            response_candles = list(map(lambda x: x['mid'], response))
            response_volume = list(map(lambda x: x['volume'], response))

            dates += response_dates
            candles += response_candles
            volume += response_volume

            _from = datetime.strftime(response_dates[-1] + timedelta(**kwarg), '%Y-%m-%dT%H:%M:00Z')
            _count = len(response)

            params.update({'from': _from,
                           'count': _count})

            time.sleep(.25)


        df = pd.DataFrame(candles, index=pd.Series(dates, name='date'))

        df = df.rename({'o': 'open',
                        'h': 'high',
                        'l': 'low',
                        'c': 'close'
                        }, axis=1)

        df['volume'] = volume
        df = df[['open', 'high', 'low', 'close', 'volume']]

        df.to_csv('oanda/data/' + granularity + '/' + currency + '.csv')
        print('Instrument updated: {}'.format(currency))

import json
import requests as r




api_key = 'oqVEAzxXwz6O9SlRhLClsxJS'

url = 'https://www.oanda.com/rates/api/v2/rates/candles.json?api_key=oqVEAzxXwz6O9SlRhLClsxJS&data_set=OANDA&base=USD&quote=NAS100USD&start_time=2017-01-01&end_time=2017-01-02'


url = 'https://www.oanda.com/rates/api/v2/currencies.json?api_key=oqVEAzxXwz6O9SlRhLClsxJS'

r.get(url).json()


# curl -X GET -H "Authorization: Bearer <API_KEY>"
# https://www.oanda.com/rates/api/v2/rates/candles.csv?base=EUR&quote=USD&start_time=2017-01-01&end_time=2017-01-02

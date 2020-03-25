
# Code for volume calculations
# Convert /BTC to /USD for alts
btc_price = btc['open']

btc['volume_usd'] = btc_price * btc['volume']
ltc['volume_usd'] = ltc['open'] * btc_price * ltc['volume']
eos['volume_usd'] = eos['open'] * btc_price * eos['volume']
eth['volume_usd'] = eth['open'] * btc_price * eth['volume']

btc['alt_volume_usd'] = ltc['volume_usd'] + eos['volume_usd'] + eth['volume_usd']

btc.head()

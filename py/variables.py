from datetime import datetime, timedelta
import time
import pygsheets
import ccxt
import os

exchange = ccxt.bitfinex()

candle_intervals = {
    '1h': 'Hourly',
    '1d': 'Daily'
}

# Telegram
API = '862004249:AAFS3xQAWRCYVbadZqr94k3sA5oqyjzmMW8'
url = 'https://api.telegram.org/bot' + API + '/sendMessage?'
chat_id = '-360419097'
test_chat_id = '-1001192596591'
atta_insiders = '@Allthingsta'
world_class = '@worldclasstrader'
world_class_elite = '-1001229157672'


tickers = ['BTC/USD','ETH/USD','ETH/BTC','BCH/BTC','LTC/BTC','XRP/USD','XRP/BTC','BCH/USD','LTC/USD','EOS/USD','EOS/BTC']

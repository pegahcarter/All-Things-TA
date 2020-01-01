## 2019.08.31
### Bot Trading Conditions
- Stop loss is based on the last 10 candles
- Spread between purchase price and SL is at least .75%, and less than 5%
- MA20 is more than .1% away from EMA40


## 2019.12.28
### Bot Trading Conditions
- Conditions for a BUY
  - 21 EMA crosses above 30 MA
  - 30 MA above 55 EMA
  - 30 MA is at least .1% above 55 EMA (Ensures price isn't whipsawing)
  - 55 EMA above 200 MA
  - SL is the lowest of the last 10 candle wicks
  - % from entry to SL is at least .75% and less than 4%
  - RSI above 50
  - In the last 12 candles, the highest wick and lowest wick are within 4% of
    each other
  - The largest candle body in the last 24 hours is smaller than 4%
  - Using the rolling standard deviation of the last 168 candle bodies
    - part1 = The largest 3 candle bodies in the last 48 hours
    - part2 = 4 * median candle body size in the last 48 hours
    - part1 - part2 has to be less than 12 * mean rolling standard deviation
      of the last 48 hours

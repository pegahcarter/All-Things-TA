import pandas as pd
from py.logic import ma, ema, macd, rsi, cross

def main():

    df = pd.read_csv('prices/BTC.csv')
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')

    df_ema_3 = ema(df['close'], window=3)
    df_ema_40 = ema(df['close'], window=40)
    df_ma_20 = ma(df['close'], window=20)
    df_macd = macd(df['close'])
    df_rsi = rsi(df['close'])

    # Logic
    intersections = cross(ema_3, ma_20)
    ema_40_above = df_ema_40 > df_ema_3 & df_ema_40 > df_ma_20
    rsi_above = df_rsi > 50
    macd_above = df_macd > 0

    for intersection in intersections:
        if intersection:
            if ema_40_above[i] & rsi_above[i] & macd_above[i]:
                signal = "buy"
            elif not ema_40_above[i] and not rsi_above[i] and not macd_above[i]:
                signal = "sell"



if __name__ == '__name__':
    main()

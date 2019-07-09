import pandas as pd
from py.logic import calc_ma, calc_ema, calc_macd, calc_rsi, cross


def main():

    for file in os.listdir('prices/'):
        df = pd.read_csv('prices/' + file)
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')

        ema_3 = calc_ema(df['close'], window=3)
        ema_40 = calc_ema(df['close'], window=40)
        ma_20 = calc_ma(df['close'], window=20)
        macd = calc_macd(df['close'])
        rsi = calc_rsi(df['close'])

        # Logic
        intersections = cross(ema_3, ma_20)
        ema_40_above = (ema_40 > ema_3) & (ema_40 > ma_20)
        rsi_above = rsi > 50
        macd_above = macd > 0

        signals = [None for x in range(len(df))]
        for i, val in enumerate(intersections):
            if val:
                if ema_40_above[i] and rsi_above[i] and macd_above[i]:
                    signals[i] = "BUY"
                elif not ema_40_above[i] and not rsi_above[i] and not macd_above[i]:
                    signals[i] = "SELL"

        df['signals'] = signals
        df.to_csv('prices/' + file, index=False)


if __name__ == '__name__':
    main()

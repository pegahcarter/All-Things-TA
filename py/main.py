import os
from py.logic import calc_ma, calc_ema, calc_macd, calc_rsi, cross
from py.functions import refresh_ohlcv, combine_signals

def main():
    df_signal = pd.DataFrame(columns=['coin', 'date', 'signal'])
    for file in os.listdir('prices/'):
        coin, df = refresh_ohlcv(file)

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

        signal = [None for x in range(len(df))]
        for i, val in enumerate(intersections):
            if val:
                if ema_40_above[i] and rsi_above[i] and macd_above[i]:
                    signal[i] = "BUY"
                elif not ema_40_above[i] and not rsi_above[i] and not macd_above[i]:
                    signal[i] = "SELL"

        df['signal'] = signal
        df.to_csv('prices/' + file, index=False)
        combine_signals(df_signal, df, coin)

    df_signal.to_csv('signals.csv', index=False)

if __name__ == '__name__':
    main()

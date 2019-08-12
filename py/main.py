import pandas as pd
import logic
from variables import *
from datetime import datetime


def main():

    for candle_abv, candle_string in candle_intervals.items():
        text = candle_string + '\n'
        signal_df = []
        for ticker in tickers:
            signal_df += logic.run(ticker, candle_abv)

        signal_df = pd.DataFrame(signal_df, columns=['date', 'ticker', 'signal', 'price', 'Stop Loss'])
        signal_df['date'] = [datetime.fromtimestamp(x/1000) for x in signal_df['date']]
        signal_df = signal_df.sort_values('date').reset_index(drop=True)
        old_signal_df = pd.read_csv('C:/Users/carter/Documents/crypto/peter-signal/signals/' + candle_string + '.csv')
        # old_signal_df = get_gsheet(candle_string)
        new_signals = signal_df[signal_df['date'] > max(old_signal_df['date'])]

        if len(new_signals) > 0:
            for _, row in new_signals.iterrows():
                if candle_string == 'Hourly':
                    date = row['date'].strftime('%m/%d %I:%M %p')
                else:  # candle_string == 'Daily'
                    date = row['date'].strftime('%m/%d')
                logic.send_signal(row, date)

            old_signal_df = old_signal_df.append(new_signals, ignore_index=True, sort=False)
            old_signal_df.to_csv('C:/Users/carter/Documents/crypto/peter-signal/signals/' + candle_string + '.csv', index=False)
            # save_gsheet(candle_string, old_signal_df)



if __name__ == '__main__':
    main()

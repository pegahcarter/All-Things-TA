
import pandas as pd
import logic
from variables import candle_intervals
from datetime import datetime


def main():

    for candle_abv, candle_string in candle_intervals.items():
        if candle_string == 'Daily' and datetime.now().hour not in [6, 7, 8]:
            break

        signal_df = logic.run(candle_abv)

        old_signal_df = pd.read_csv('/home/carl/Documents/crypto/peter-signal/signals/' + candle_string + '.csv')
        new_signals = signal_df[signal_df['date'] > max(old_signal_df['date'])]

        if len(new_signals) > 0:
            for _, row in new_signals.iterrows():
                logic.send_signal(row, candle_string)

            old_signal_df = old_signal_df.append(new_signals, ignore_index=True)
            old_signal_df.to_csv('/home/carl/Documents/crypto/peter-signal/signals/' + candle_string + '.csv', index=False)


if __name__ == '__main__':
    main()

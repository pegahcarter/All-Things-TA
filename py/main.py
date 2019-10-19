import pandas as pd
import logic
from datetime import datetime
from variables import channels


def main():
    for channel in channels:
        # if channel['name'] == 'atta_insiders':
        #     break

        signal_df = logic.run(channel)
        # signal_df.to_csv('C:/Users/carter/Documents/crypto/peter-signal/data/signals/' + channel['name'] + '.csv', index=False)

        old_signal_df = pd.read_csv('C:/Users/carter/Documents/crypto/peter-signal/data/signals/Hourly.csv')
        # old_signal_df = pd.read_csv('C:/Users/carter/Documents/crypto/peter-signal/data/signals/' + channel['name'] + '.csv')
        new_signals = signal_df[signal_df['date'] > max(old_signal_df['date'])]

        if len(new_signals) > 0:
            old_signal_df = old_signal_df.append(new_signals, ignore_index=True, sort=False)
            old_signal_df.to_csv('C:/Users/carter/Documents/crypto/peter-signal/data/signals/Hourly.csv', index=False)
            # old_signal_df.to_csv('C:/Users/carter/Documents/crypto/peter-signal/data/signals/' + channel['name'] + '.csv', index=False)

            for _, row in new_signals.iterrows():
                logic.send_signal(row, channel)


if __name__ == '__main__':
    main()

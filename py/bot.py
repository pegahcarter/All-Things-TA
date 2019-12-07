import pandas as pd
import logic
from datetime import datetime


channels = {
    'wc_elite': [21, 30, 55]
   # 'atta_insiders': [8, 25, 50]
}


def main():
    for channel, averages in channels.items():

        signal_df = logic.run(averages)

        old_signal_df = pd.read_csv('/home/carter/peter-signal/data/signals/' + channel + '.csv')
        new_signals = signal_df[signal_df['date'] > max(old_signal_df['date'])]

        if len(new_signals) > 0:
            old_signal_df = old_signal_df.append(new_signals, ignore_index=True, sort=False)
            old_signal_df.to_csv('/home/carter/peter-signal/data/signals/' + channel + '.csv', index=False)

            for _, row in new_signals.iterrows():
                logic.send_signal(row, channel)


if __name__ == '__main__':
    main()

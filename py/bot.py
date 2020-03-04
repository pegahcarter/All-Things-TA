from config import channels

import logic

import pandas as pd

from datetime import datetime

import os


def main(testing=False):

    for channel, averages in channels.items():

        # Create dataframe of signals based on algorithm logic
        signal_df = logic.run(averages)

        # Load past saved signals
        csv_filename = f"{os.path.abspath('../')}/data/signals/{channel}.csv"
        old_signal_df = pd.read_csv(csv_filename)

        # Compare our signals dataframe to the saved signals dataframe
        # Only look at signals that are more recent than the saved signals
        new_signals = signal_df[signal_df['date'] > max(old_signal_df['date'])]

        if len(new_signals) > 0:
            old_signal_df = old_signal_df.append(new_signals, ignore_index=True, sort=False)
            old_signal_df.to_csv(csv_filename, index=False)

            if not testing:
                for _, row in new_signals.iterrows():
                    logic.send_signal(row, channel)



if __name__ == '__main__':
    main()
    # TODO: CLI with python arguments

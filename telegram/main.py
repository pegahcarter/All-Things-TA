

def main():

    # Loop through channels for signals
    for channel_name, channel_averages in channels.items():

        # Create signals DataFrame
        signal_df = signals(channel_averages)


def signals(ticker):
    pass


if __name__ == "__main__":
    main()

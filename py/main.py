

def ma(data, period):
    pass


def ema(data, period):
    pass


def macd(data):
    pass


def rsi(data):
    pass

def main():

    ''' EMA '''
    # 3 period EMA
    ema(data, period=3)
    # 40 period EMA
    ema(data, period=40)

    ''' MA '''
    # 20 period MA
    ma(data, period=20)

    ''' MACD '''
    # What period should this be?
    macd(data)

    ''' RSI '''
    # What period should this be?
    rsi(data)

    ''' Logic '''



if __name__ == '__name__':
    main()

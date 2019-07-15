import os
import pandas as pd
import py.logic as logic
from datetime import datetime, timedelta
from time import sleep

coins = ['BTC', 'ETH', 'LTC', 'BCH', 'BNB']

def main():
    while True:
        sleep(45)
        if datetime.now().minute == 1:
            sleep(60)



if __name__ == '__name__':
    main()

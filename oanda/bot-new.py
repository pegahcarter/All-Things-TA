import requests
from urllib.parse import urlencode


class Bot:

    API = '862004249:AAFS3xQAWRCYVbadZqr94k3sA5oqyjzmMW8'
    base_url = 'https://api.telegram.org/bot' + API + '/sendMessage?'
    chat_id = '-360419097'
    test_id = '-1001192596591'
    wc_id = '@worldclasstrader'
    wc_elite_id = '-1001229157672'
    atta_id = '@AllthingsTA'
    atta_insiders_id = '-1001456456400'

    def __init__(self, *args, **kwargs):
        pass


    def build_message(self, channel, row):

        price = row['price']
        stop_loss = row['stop_loss']
        ticker = row['ticker']
        signal = row['signal']

        if channel == 'wc_elite':
            price *= .9998
            low_price, high_price = buy_range(price, diff=.0012)
        else:  # channel == 'ata_insiders'
            low_price, high_price = buy_range(price, diff=.0011)

        diff = price - stop_loss
        tps = [price + diff/2., price + diff, price + diff*2]

        low_price = stringify_num(channel, ticker, low_price)
        high_price = stringify_num(channel, ticker, high_price)
        tps  = [stringify_num(channel, ticker, tp) for tp in tps]
        stop_loss = stringify_num(channel, ticker, stop_loss)

        # Send primary message
        chat_id = getattr(self, channel)
        self.send_message(chat_id, message)

        # Send message to free WC channel
        if ticker in ['XRP/H20', 'ETH/USD', 'LTC/H20', 'BCH/H20']:
            self.send_message(self.wc_id, message)

        # Send message to free ATTA channel
        if ticker in ['BTC/USD', 'ETH/USD', 'ETH/H20']:
            self.send_message(self.atta_id, message)


    def template(self, channel, ticker, signal, stop_loss, low_price, high_price, tps):
        # build template
        if 'wc' in channel:
            message = '🚨🚨🚨\n\n'
            message += '{}\nBitMEX\n'.format(ticker)
            message += '{} zone {}-{}\n'.format(signal, low_price, high_price)
            message += 'Take profit {}, {}, {}\n'.format(*tps)
            message += 'Leverage 10x\n'
            message += 'Stop loss {}\n\n'.format(stop_loss)
            message += '🚨🚨🚨'
        else:   # channel == 'atta'
            message = '🚀🚀{}🚀🚀\n\n'.format(ticker)
            message += 'BitMEX' + '\n\n{} '.format(signal)
            message += '{} - {}\n\n'.format(low_price, high_price)
            message += 'Sell {}, {}\n\n'.format(tps[0], tps[1])
            message += 'Leverage 5x\n\n'
            message += 'Stop Loss: {}\n\n'.format(stop_loss)
            message += '*Disclaimer: Please consult a financial advisor before investing/trading.  This is not financial advice🚀🚀\n\n'
            message += '💰💰@Allthingstaadmin💰💰'
        return message


    def send_message(self, chat_id, message):
        message =
        url = self.base_url + urlencode({'chat_id': chat_id, 'message': message})
        return requests.get(url)


    def buy_range(self, price, diff=0):
        low_price = price * (1. - diff)
        high_price = price * (1. + diff)
        return low_price, high_price


    def stringify_num(self, channel, ticker, number):
        if ticker == 'ETH/USD':
            return format(number, '.2f')
        else:
            decimals = self.determine_decimals(ticker)
            if 'wc' in channel:
                return format(number, '.' + str(decimals) + 'f')
            else:  # channel == 'atta'
                return str(int(number * 10**decimals))


    def determine_decimals(self, ticker):
        if ticker == 'BTC/USD':
            decimals = 0
        elif 'BCH' in ticker or 'ETH' in ticker:
            decimals = 5
        elif 'LTC' in ticker:
            decimals = 6
        elif 'EOS' in ticker:
            decimals = 7
        elif 'XRP' in ticker:
            decimals = 8
        return decimals

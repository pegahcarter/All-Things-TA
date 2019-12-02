from functions import *
from portfolio import Portfolio

signals = []
tp_pcts = {1: 10, 2: 10, 3: 10, 4: 70}

for f in os.listdir('../data/binance/'):

    df = pd.read_csv('../data/binance/' + f)
    coin_signals = find_signals(df, 21, 30, 50)

    # Add `tp`, `index_tp_hit`, and `index_closed`
    determine_TP(df, coin_signals)

    # Add ticker & pct_open to signal
    for x in coin_signals:
        x.update({
            'ticker': f[:f.find('.')],
            'pct_open': 100
        })

    # Add coin signals to the primary signal list
    signals.extend(coin_signals)

# Re-order signals by `index_opened`
signals_sorted = list(sorted(signals, key=lambda x: x['index_opened']))

class Portfolio:

    initial_capital = 10000
    x_leverage = 1
    trade_size = .1

    def __init__(self, *args, **kwargs):
        self.available_capital = self.initial_capital
        self.positions = []
        self.index_tp_hit_set = set()
        self.index_closed_set = set()

    def positions_open(self):
        return len(self.positions)

    def open_position(self, **position):
        position['d_amt'] = self.available_capital * self.trade_size * self.x_leverage
        self.available_capital -= position['d_amt']

        self.index_tp_hit_set.update(position['index_tp_hit'])
        self.index_closed_set.add(position['index_closed'])
        self.positions.append(position)

    def close_position(self, x_leverage, **position):
        self.available_capital += position['d_amt'] * (1 + position['net_profit'] * x_leverage)
        return self.positions.pop(self.positions.index(position))



p = Portfolio()

# Add test position
p.open_position(**signals_sorted[0])
p.open_position(**signals_sorted[1])
p.positions


list(filter(lambda x: 68 in x['index_tp_hit'], p.positions))

# Sell 10% of position at TP1
# if 68 in p.index_tp_hit_set:

# TODO: remove [0] from line below when looping through entire portfolio, and
#   rename `p` as `positions_to_sell`
p = list(filter(lambda x: 68 in x['index_tp_hit'], p.positions))[0]

# for p in positions_to_sell:
while 68 in p['index_tp_hit']gfh






# Old code
# for i, date in enumerate(btc['date']):
#
#     if sum(signals['date'] == date):
#         for _, position in signals[signals['date'] == date].iterrows():
#             portfolio.open_position(pct_capital=.05, **position)
#
#     if sum(signals['index_closed'] == i):
#         for position in list(filter(lambda x: x['index_closed'] == i, portfolio.positions)):
#             portfolio.close_position(x_leverage=5, **position)
#
#
# for position in portfolio.positions:
#     portfolio.close_position(x_leverage=5, **position)

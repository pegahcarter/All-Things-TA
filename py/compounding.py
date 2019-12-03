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
signals_sorted_copy = list(sorted(signals, key=lambda x: x['index_opened']))

class Portfolio:

    initial_capital = 10000
    x_leverage = 10
    trade_size = .1
    profit_levels = [.5, 1, 2, 3]

    def __init__(self, tp_pcts):
        self.available_capital = self.initial_capital
        self.positions = []
        self.tp_pcts =  tp_pcts
        self.index_tp_hit_set = set()
        self.index_closed_set = set()

    def positions_open(self):
        return len(self.positions)

    def open_position(self, position):
        d_amt = self.available_capital * self.trade_size
        self.available_capital -= d_amt
        position['d_amt'] = d_amt * self.x_leverage

        self.index_tp_hit_set.update(position['index_tp_hit'])
        self.index_closed_set.add(position['index_closed'])
        self.positions.append(position)

    def sell_position(self, hr, position):
        pos = position['index_tp_hit'].index(hr)
        profit_level = self.profit_levels[pos]
        pct_sold = self.tp_pcts[pos + 1]

        base_sold = position['d_amt'] * pct_sold/100
        profit = base_sold * position['pct_open'] * position['pct'] * profit_level / 100

        base_sold /= self.x_leverage

        position['pct_open'] -= pct_sold
        position['index_tp_hit'][pos] = None

        self.available_capital += base_sold + profit


    def close_position(self, position):

        # self.positions.pop(self.positions.index(position))
        pct_sold = position['pct_open']

        base_sold = position['d_amt'] * pct_sold/100
        if position['tp'] == 4:
            return
        elif position['tp'] == 0:
            profit = -base_sold * position['pct']
        else:
            profit = 0

        base_sold /= self.x_leverage

        self.available_capital += base_sold + profit


p = Portfolio(tp_pcts)
i = 0

for hr in range(16000):

    # Opening positions
    while len(signals_sorted) > 0 and signals_sorted[0]['index_opened'] == hr:
        p.open_position(signals_sorted.pop(0))

    if p.positions_open():
        # Selling part of positions
        if hr in p.index_tp_hit_set:
            for position in filter(lambda x: hr in x['index_tp_hit'], p.positions):
                while hr in position['index_tp_hit']:
                    p.sell_position(hr, position)

        # Closing out positions
        if hr in p.index_closed_set:
            for position in filter(lambda x: hr == x['index_closed'], p.positions):
                i += 1
                p.close_position(position)


p.available_capital
len(p.positions)
i


net_profit(signals, tp_pcts)

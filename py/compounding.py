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
            for position in list(filter(lambda x: hr == x['index_closed'], p.positions))[::-1]:
                i += 1
                p.close_position(position)


p.available_capital
len(p.positions)
i


net_profit(signals, tp_pcts)

from functions import *
from portfolio import Portfolio
from variables import avgs_combined

available_capital_lst = []
tp_pcts = {1: 10, 2: 10, 3: 10, 4: 70}

results = pd.DataFrame()
results['average'] = avgs_combined


for avgs in avgs_combined[::40]:
    signals = []

    for coin in ['ETH-USDT', 'BTC-USDT']:

        df = pd.read_csv('../data/binance/' + coin + '.csv')
        coin_signals = find_signals(df, *avgs)

        # Add `tp`, `index_tp_hit`, and `index_closed`
        determine_TP(df, coin_signals)

        # Add ticker & pct_open to signal
        for x in coin_signals:
            x.update({
                # 'ticker': f[:f.find('.')],
                'ticker': coin,
                'pct_open': 100
            })

        # Add coin signals to the primary signal list
        signals.extend(coin_signals)

    # Re-order signals by `index_opened`
    signals_sorted = list(sorted(signals, key=lambda x: x['index_opened']))

    p = Portfolio(tp_pcts)

    for hr in range(16000):

        # Opening positions
        while len(signals_sorted) > 0 and signals_sorted[0]['index_opened'] == hr:
            p.open_position(signals_sorted.pop(0))

        if p.positions_open():

            # Selling part of positions
            if hr in p.index_tp_hit_set:
                for position in list(filter(lambda x: hr in x['index_tp_hit'], p.positions)):
                    while hr in position['index_tp_hit']:
                        p.sell_position(hr, position)

            # Closing out positions
            if hr in p.index_closed_set:
                for position in list(filter(lambda x: hr == x['index_closed'], p.positions))[::-1]:
                    p.close_position(position)

    available_capital_lst.append(p.available_capital)


available_capital_lst

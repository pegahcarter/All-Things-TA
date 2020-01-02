# Finds compounding results with different moving averages and tp_pct
from functions import *
from portfolio import Portfolio
from variables import avgs_combined, tp_pcts_list
import itertools
import os
import ujson


results = pd.DataFrame(index=['-'.join(str(int(x*100)) for x in tp_pcts[1:]) for tp_pcts in tp_pcts_list])


for avgs in avgs_combined:

    signals = []
    for f in os.listdir('../data/binance/'):

        df = pd.read_csv('../data/binance/' + f)
        coin_signals = find_signals(df, *avgs)

        # Add `tp`, `index_tp_hit`, and `index_closed`
        determine_TP(df, coin_signals)

        # Add ticker to signal & remove unused keys
        ticker = f[:f.find('.')]
        for x in coin_signals:
            x.update({'ticker': ticker})
            x.pop('date')
            x.pop('price')
            x.pop('stop_loss')

        # Add coin signals to the primary signal list
        signals.extend(coin_signals)

    # Re-order signals by index opened
    signals = sorted(signals, key=lambda x: x['index_opened'])

    indices_tp_hit = set(itertools.chain.from_iterable(map(lambda x: x['index_tp_hit'], signals)))
    indices_tp_hit.remove(None)
    indices_opened = set(map(lambda x: x['index_opened'], signals))
    indices_closed = set(map(lambda x: x['index_closed'], signals))
    indices_of_action = sorted(indices_opened | indices_tp_hit | indices_closed)

    available_capital_lst = []
    for tp_pcts in tp_pcts_list:

        signals_copy = ujson.loads(ujson.dumps(signals))
        portfolio = Portfolio(tp_pcts)

        for index_of_action in indices_of_action:

            # Opening positions
            while len(signals_copy) > 0 and signals_copy[0]['index_opened'] == index_of_action:
                portfolio.open(signals_copy.pop(0))

            # Selling positions
            if index_of_action in indices_tp_hit:
                for position in filter(lambda x: index_of_action in x['index_tp_hit'], portfolio.positions):
                    while index_of_action in position['index_tp_hit']:
                        portfolio.sell(position, index_of_action)

            # Closing positions
            if index_of_action in indices_closed:
                for position in list(filter(lambda x: index_of_action == x['index_closed'], portfolio.positions))[::-1]:
                    portfolio.close(position)


        # Save ending portfolio value
        available_capital_lst.append(portfolio.available_capital)

    # Save all TP outcomes for moving average combination
    results['-'.join(str(x) for x in avgs)] = available_capital_lst

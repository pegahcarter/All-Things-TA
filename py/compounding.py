from functions import *
from portfolio import Portfolio
from variables import avgs_combined, tp_pcts_lst

results = pd.DataFrame(index=['-'.join(str(x) for x in tp_pcts.values()) for tp_pcts in tp_pcts_lst])

for avgs in avgs_combined:

    available_capital_lst = []
    for tp_pcts in tp_pcts_lst:

        signals = []
        for f in os.listdir('../data/binance/'):

            df = pd.read_csv('../data/binance/' + f)
            coin_signals = find_signals(df, *avgs)

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
        signals_sorted = list(sorted(signals.copy(), key=lambda x: x['index_opened']))
        portfolio = Portfolio(tp_pcts)

        for hr in range(16000):

            # Opening positions
            while len(signals_sorted) > 0 and signals_sorted[0]['index_opened'] == hr:
                portfolio.open_position(signals_sorted.pop(0))

            if len(portfolio.positions) > 0:

                # Selling part of positions
                if hr in portfolio.index_tp_hit_set:
                    for position in list(filter(lambda x: hr in x['index_tp_hit'], portfolio.positions)):
                        while hr in position['index_tp_hit']:
                            portfolio.sell_position(hr, position)

                # Closing out positions
                if hr in portfolio.index_closed_set:
                    for position in list(filter(lambda x: hr == x['index_closed'], portfolio.positions))[::-1]:
                        portfolio.close_position(position)

        available_capital_lst.append(portfolio.available_capital)


    results['-'.join(str(x) for x in avgs)] = available_capital_lst


results.to_csv('../backtests/data/2019.12.06.csv')

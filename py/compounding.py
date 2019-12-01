from functions import *
from portfolio import Portfolio

signals = []
tp_pcts = {1: 10, 2: 10, 3: 10, 4: 70}

for f in os.listdir('../data/binance/'):

    df = pd.read_csv('../data/binance/' + f)
    coin_signals = find_signals(df, 21, 30, 50)

    # Add `tp`, `index_tp_hit`, and `index_closed`
    determine_TP(df, coin_signals)

    # Add ticker to signal
    [x.update({'ticker': f[:f.find('.')]}) for x in coin_signals]

    # Add coin signals to the primary signal list
    signals.extend(coin_signals)

# Re-order signals by `index_opened`
signals_sorted = list(sorted(signals, key=lambda x: x['index_opened']))

signal = signals_sorted[0]

#

signal






portfolio = Portfolio()

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

import pandas as pd
from signals import signals


def profit(signals):
    profit_pct = [-1, 0.025, 0.95]

    _profit = list(map(lambda x: profit_pct[x['tp']] * x['pct'], s))

    return _profit

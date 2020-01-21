### Algorithm analysis
#### By: Carter Carlson


#### Algorithm Description
* Max drawdown over 30 days:  26.58%
* Max upside over 30 days: 38.03%
* Size per trade: 10% of available capital
* Leverage: 10x
* Max gain/loss possible per trade: 4% of portfolio
* Max percent of portfolio locked in trades:  44.79%
* Max # of trades open at one time:  6


---

#### Risk vs. Reward based on Profit (TP)
|   TP    | Risk/Reward |
|---------|-------------|
|   0     |    -1:1     |
|   1     |    .5:1     |
|   2     |     1:1     |

---

#### Algorithm comparison
- `A` : Base algorithm
- `B` : Base algorithm with custom logic


|   TP    |    `A`    |    `B`    |   Change   |
|---------|-----------|-----------|------------|
|   0     |  27.84%   |  22.77%   |   -5.07%   |
|   1     |  32.77%   |  34.48%   |    1.71%   |
|   2     |  39.39%   |  42.75%   |    3.36%   |

---

#### Compounded results
* Timeframe: Feb 10, 2018 - Dec 31, 2019

# TODO: fix profit per trade

|       | Start Value (BTC) | End Value (BTC) |  Net Profit | Trade Count | Avg. profit per trade (including fees)|
|-------|-------------------|-----------------|-----------|-------------| ----------------------|
|  `A`  |    10             |     5.02        |  -49.08%   |   1801      |         0.0084%       |
|  `B`  |    10             |    40.01        |  400.01%   |    786      |         0.1074%        |


---
#### Conclusions
* Net profit __increased over 5x__ (15.1% => 84.40%)
* Trade count __reduced over 50%__ (1801 => 786)
* Average profit per trade __increased over 10x__ (0.0084% => 0.1074%)


#### Analyze trade size and removing trade %'s that are `x` standard deviations
- Create signal data for all Binance pairs with no trade size requirements
- Current trade requirements remove this much % of data
  - trade_size < 0.0075%  =>  4.87% of all trades
  - trade_size > 0.04%    =>  10.1% of all trades


#### Risk vs. Reward based on Profit (TP)
|   TP    | Risk/Reward |
|---------|-------------|
|   0     |    -1:1     |
|   1     |    .5:1     |
|   2     |     1:1     |
|   3     |     2:1     |
|   4     |     3:1     |

---

#### Algorithm comparison
- `A` : Base algorithm
- `B` : Base algorithm with custom logic
- `C` : Base algorithm with custom logic and trade size requirements

|   TP    |    `A`    |    `B`    |    `C`    |   Change   |
|---------|-----------|-----------|-----------|------------|
|   0     |  27.56%   |  23.26%   |  21.92%   |   -5.64%   |
|   1     |  32.43%   |  34.59%   |  34.53%   |    2.10%   |
|   2     |  17.27%   |  17.42%   |  17.33%   |    0.06%   |
|   3     |   6.23%   |   6.58%   |   6.59%   |    0.36%   |
|   4     |  16.51%   |  18.15%   |  19.63%   |    3.12%   |

#### Number of trades

|       | Trade Count |
|-------|-----------  |
|  `A`  |   1702      |
|  `B`  |    821      |
|  `C`  |    698      |


#### Compounded results(March 2018 - Nov 2019 with a starting value of $10k)

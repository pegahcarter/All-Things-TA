
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



#### Compounded results
* Jan 2019 - Nov 2019
* For all tickers on BitMEX
* Starting value: $10k
|       | Start Value ($)   | End Value ($)      |   % change | Trade Count | Avg. profit per trade (after fees)|
|-------|-----------        |--------------------| --------   |-----------  | ----------------------|
|  `A`  |    10,000         |    11,183.35       |  11.18%    |   1702      |         0.0065%       |
|  `B`  |    10,000         |    15,997.49       |  59.97%    |    821      |         0.07%         |
|  `C`  |    10,000         |    19,381.38       |  93.81%    |    698      |         0.13%         |


* 0.0065% profit per trade => 0.13% profit per trade is an improvement of __20x__




#### Max drawdown (30 day)
|       | Max drawdown % | Max drawdown date   |
|-------|-----------   |-------------------|
|  `A`  |    62.2%    |2019-08-01 13:00:00|
|  `B`  |    51.7%    |2019-08-25 05:00:00|
|  `C`  |    50.3%    |2019-07-03 12:00:00|

#### Conclusions
* Decreased trade size by 60%
* Reduce SL's hit by 5% and increase wins by 5% (10% net)
* Added 82.6% in profit after fees
* Reduced max drawdown by 12%

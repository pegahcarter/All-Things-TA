### Algorithm analysis
#### By: Carter Carlson


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


|       | Start Value (BTC) | End Value (BTC) |  Net Profit | Trade Count | Avg. profit per trade (including fees)|
|-------|-------------------|-----------------|-----------|-------------| ----------------------|
|  `A`  |    10             |    11.51        |  15.10%   |   1801      |         0.0084%       |
|  `B`  |    10             |    18.84        |  84.40%   |    786      |         0.1074%        |


---
#### Conclusions
* Net profit __increased over 5x__ (15.1% => 84.40%)
* Trade count __reduced over 50%__ (1801 => 786)
* Average profit per trade __increased over 10x__ (0.0084% => 0.1074%)

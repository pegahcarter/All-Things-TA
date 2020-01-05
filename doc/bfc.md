
#### Analyze trade size and removing trade %'s that are `x` standard deviations
- Create signal data for all Binance pairs with no trade size requirements
- Current trade requirements remove this much % of data
  - trade_size < 0.0075%  =>  4.87% of all trades
  - trade_size > 0.04%    =>  10.1% of all trades


#### Custom Standard Deviation Parameters
|   TP    | Risk/Reward |   No requirement  |
|---------|-------------|-------------------|
|   0     |    -1:1     |      23.26%       |
|   1     |    .5:1     |      34.59%       |
|   2     |     1:1     |      17.42%       |
|   3     |     2:1     |      06.58%       |
|   4     |     3:1     |      18.15%       |









#### Profit Distribution
|   TP    | Risk/Reward |   No requirement  |   0.75% < trade size < 4.0%   |   Change   |
|---------|-------------|-------------------|-------------------------------|------------|
|   0     |    -1:1     |      23.26%       |            21.92%             |   -1.34%   |
|   1     |    .5:1     |      34.59%       |            34.53%             |   -0.06%   |
|   2     |     1:1     |      17.42%       |            17.33%             |   -0.09%   |
|   3     |     2:1     |      06.58%       |            06.59%             |   -0.01%   |
|   4     |     3:1     |      18.15%       |            19.63%             |   1.48%    |


#### Trade size requirement: None
- Distribution
  - count           821
  - mean          1.94%
  - std           1.21%
  - min           0.29%
  - max           12.3%

#### Trade size requirement:  `0.75% < trade size < 4.0%`
- Distribution
  - count      698
  - mean     1.90%
  - std      0.79%
  - min      0.75%
  - max       3.9%






### 2020.01.04
  - Question: How would you go about deciding what % to remove?  Would you ...
    - Look at compounding or absolute return?
    - Apply a universal model for all exchange pairs? Or custom parameters per pair?
    - Use standard deviation to remove trade size outliers?  Number other than sdev?

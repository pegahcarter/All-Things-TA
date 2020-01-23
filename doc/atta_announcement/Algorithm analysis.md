ATTA Algorithm Summary
======================
[@AllthingsTA](https://t.me/AllthingsTA)
----------------------


&nbsp; | &nbsp;
------ | -----
Max drawdown over 30 days |  14%
Max upside over 30 days | 17%
Available capital allocated per trade | 10%
Leverage | 5x
Max gain/loss possible per trade | 2%
Max percent of portfolio locked in trades |  44.79%
Max # of trades open at one time |  6
Average trade duration | 12 hours
Average time between trades | 21 hours


Risk vs. Reward based on Profit (TP)
======================
   TP    | Risk/Reward
---------|-------------
   0     |    -1:1     
   1     |    .5:1     
   2     |     1:1     


Algorithm comparison
======================
- `A` : Base algorithm
- `B` : Base algorithm with custom logic


   TP    |    `A`    |    `B`    |   Change   
---------|-----------|-----------|------------
   0     |  27.84%   |  22.77%   |   -5.07%   
   1     |  32.77%   |  34.48%   |    1.71%   
   2     |  39.39%   |  42.75%   |    3.36%   


Compounded results
======================
* Timeframe: Feb 10, 2018 - Dec 31, 2019



 &nbsp;| Start Value (BTC) | End Value (BTC) |  Net Profit | Trade Count | Avg. profit per trade (including fees)
-------|-------------------|-----------------|-------------|-------------| ----------------------
  `A`  |    1              |     0.81        |  -19%    |   1801      |         -0.011%       
  `B`  |    1              |     2.06         |  106%    |    786      |         0.262%        


Conclusions
======================
* Loss rate __reduced by ~5%__ and win rate __improved by ~5%__
* Net profit __changed from -19% to +106%__
* Trade count __reduced over 50%__ (1801 => 786)
* Average profit per trade __improved by a factor of over 20x__ (-0.011% => 0.262%)

To long:
- 3 crosses 20
- 20 > 40 ema
- rsi > 50
- MACD > 0


### 2019.08.08

- Figure out setting TP
  - TP1:
    - .5 * SL
    - Adjust SL to buy-in price
  - TP2:
    - SL
  - TP3:
    - SL * 2
  - TP4:
    - SL * 3

TP column:
  - 0: hit SL before TP
  - 1-4: based on TP level

### 2019.08.10
### TP Example
- Buy 1 BTC @ 10,000 (\$)
- SL @ 9,800

### TP Levels:
  - TP0 (SL): 9,800
  - TP1: 10,100
  - TP2: 10,200
  - TP3: 10,400
  - TP4: 10,600

### Profit Levels:
  - TP0: (9,800 - 10,000) * 100% = __- \$200__
  - TP1: (10,100 - 10,000) * 25% = __+ \$25__
  - TP2: (10,100 - 10,000) * 25% + (10,200 - 10,000) * 25% = __+ \$75__
  - TP3: (10,100 - 10,000) * 25% + (10,200 - 10,000) * 25% + (10,400 - 10,000) * 25% = __+ \$175__
  - TP4: (10,100 - 10,000) * 25% + (10,200 - 10,000) * 25% + (10,400 - 10,000) * 25%  + (10,600s - 10,000) * 25% = __+ \$325__

### Risk vs. Reward
risk = __$200__
reward = 25 + 75 + 175 + 325 = __$600__
reward/risk = 600 / 200 = __3.00__

### Profit compared to starting SL (\$200)
  - TP0: -200 / 200 = __- 1__
  - TP1: 25 / 200 =  __+ 1/8__
  - TP2: 75 / 200 = __+ 3/8__
  - TP3: 175 / 200 = __+ 7/8__
  - TP4: 325 / 200 = __+ 13/8__

- Calculating TP
  - 0: -(100% * SL_pct)
  - TP1: (25% * SL_pct/2)
  - TP2: (25% * SL_pct/2) + (25% * SL_pct)
  - TP3:
  - TP4:

- Additional columns for ML training
  1. Average Slope
    a. Slope of all 3 averages (separate)
    b. Compare 3-20 slope
    c. Compare 20-40 slope
  2. Hours since last same-signal signal
  3. Hours since last opposite-signal signal

### 2019.08.20
### Deciding different TP %

### TP Example
  TP1: sell 40%
  TP2: sell 20%
  TP3: sell 20%
  TP4: sell 20%

### Profit Levels:
  - TP0: (9,800 - 10,000) * 100% = __- \$200__
  - TP1: (10,100 - 10,000) * 40% = __+ \$40__
  - TP2: (10,100 - 10,000) * 40% + (10,200 - 10,000) * 20% = __+ \$80__
  - TP3: (10,100 - 10,000) * 40% + (10,200 - 10,000) * 20% + (10,400 - 10,000) * 20% = __+ \$160__
  - TP4: (10,100 - 10,000) * 40% + (10,200 - 10,000) * 20% + (10,400 - 10,000) * 20%  + (10,600 - 10,000) * 20% = __+ \$280__

### Generalized TP formula
  - tp1_pct = (tp1 / 2)
  - tp2_pct = tp1_pct + tp2
  - tp3_pct = tp2_pct + (2 * tp3)
  - tp4_pct = tp3_pct + (3 * tp4)



### 2019.11.05
#### Take Profit levels for ATTA
  - R/R for 20-20-20-40 if closed at each TP
    - Assume we enter @ 10000 and SL @ 9800
    - TP0: -1   ->  (9800 - 10000) * 1
    - TP1: 0.1  -> (10100 - 10000) * 0.2
    - TP2: 0.3  -> tp1 + (10200 - 10000) * 0.2
    - TP3: 0.8  -> tp1 + tp2 + (10400 - 10000) * 0.2
    - TP4: 2.4  -> tp1 + tp2 + tp3  + (10600 - 10000) * 0.4     



### 2019.11.18
#### TP ERROR?!?
  - Realized TP2 and on assumes we profit based on 100% of our trade value
  - Selling 20% at TP1 means we're only making profit on 80% our trade value if we close
      at TP2...

### Correct TP Logic

  - TPS: 0.5:1, 1:1, 2:1, 3:1
  - price = 10000
  - pct = .03

  - Example 1:
    - tp1 = price * pct * 0.5 * .25 * 1.0  = 37.50
    - tp2 = price * pct * 1.0 * .25 * .75  = 56.25
    - tp3 = price * pct * 2.0 * .25 * .50  = 75.00
    - tp4 = price * pct * 3.0 * .25 * .25  = 56.25
  - Example 2:
    - sell_pct = [.25, .25, .25, .25]
    - tps = [.5, 1, 2, 3]
    - tp1 = pct * tps[0] * (1 - sum(sell_pct[:0])) * sell_pct[0]
    - tp2 = pct * tps[1] * (1 - sum(sell_pct[:1])) * sell_pct[1]
    - tp3 = pct * tps[2] * (1 - sum(sell_pct[:2])) * sell_pct[2]
    - tp4 = pct * tps[3] * (1 - sum(sell_pct[:3])) * sell_pct[3]

  - tp1 + tp2 + tp3 + tp4 = 225


### 2019.11.21
#### Train of thought for new backtests
- Ensure TP logic is correct
- Use COMPOUNDING return, not absolute return
  - For each backtested trade, get TP, index opened, and index closed
  - Use index opened to indicate opening trade
  - Close % of trade at each TP
  - Use a # for % of trade open?
  - Changes per TP


### 2019.11.27
#### Train of thought to execute backtest improvement
- Optimize fetch_signals & add functions from fx-signal
- Review Bitmex fees
- Super simple compounding
  - Use TP - 1 for indexing closing position


### 2019.11.30
#### Compounding Logic
- Closing a position
  - SL will close on `index_closed`
  - TP1 - TP3 will close on `index_closed`
  - TP4 will close on `index_closed` OR `index_tp_hit[-1]`


### 2019.12.01
#### Thoughts for funding
- Only real remaining work to get ATTA/WC profitable is on my end
- Carter has been spending ~20 hrs a week on this project
- Work load has been proportionally higher on my end
- Total payment: .2 BTC / $2,000

#### Fee Structure
- Options
  - 6 months - .035 BTC
  - Lifetime - .055 BTC

#### ATTA Earning Potential
- Insiders: 183 total members - 150 "real" members
  - Assume 10% of members renew for 6 months, and 5% renew for a lifetime
    - 6 month revenue = 150 members * 10% * .035 = .525 BTC
    - Lifetime revenue = 150 members * 5% * .055 = .413 BTC
    __- Total:  .938 BTC__
- Free: 2,923 total members - 2,500 "real" members
  - Assume 4% subscribe for 6 months, and 2% subscribe for a lifetime
    - 6 month revenue = 2,500 members * 4% * .035 = 3.5 BTC
    - Lifetime revenue = 2,500 members * 2% * .055 = 2.75 BTC
    __- Total: 6.25 BTC__
__- Net Profit: .938 BTC + 6.5 BTC = 7.188 BTC or 1.8 BTC each__

#### Order of Execution
1. Fix & improve WC/ATTA signals immediately
2. Start generating income from WC/ATTA
  - WC

#### Cost of work
- September to end of December = 4 months or 16 weeks
- 20 hrs/week * 16 weeks = 320 hrs
- Pay for an entry data scientist ~ $100k/yr or $50/hr
- 320 hrs * $50/hr = $16,000
- Already paid: .2 BTC or $2,000
- Remaining cost = $14,000

#### Proposal
1.
  - Upfront payment of $5,000 for September - December work
  - For the first 10 BTC of subscriptions:
    - George, George, and Peter reduce percent by 5% (from 25% to 20%), Carter goes to 40%
      - Before: 2.5 BTC for George, George, Peter, and Carter
      - After: 2 BTC for George, George, and Peter, 4 BTC for Carter
    - Carter's BTC profit goes from 2.5 BTC => 4 BTC, profit of 1.5 BTC
  - Total: $5,000 and 1.5 BTC
2.
  - Upfront payment of $7,500 for September - December work
  - For the first 5 BTC of subscriptions:
    - George, George, and Peter reduce percent by 5% (from 25% to 20%), Carter goes to 40%
      - Before: 1.25 BTC for George, George, Peter, and Carter
      - After: 1 BTC for George, George, and Peter, 2 BTC for Carter
    - Carter's BTC profit goes from 1.25 BTC => 2 BTC, profit of .75 BTC
  - Total: $7,500 and .75 BTC
3.
  - Upfront payment of $10,000 for September - December work
  - For the first 2 BTC of subscriptions:
    - George, George, and Peter reduce percent by 5% (from 25% to 20%), Carter goes to 40%
      - Before: 0.5 BTC for George, George, Peter, and Carter
      - After: 0.4 BTC for George, George, and Peter, .8 BTC for Carter
    - Carter's BTC profit goes from .5 BTC => .8 BTC, profit of .3 BTC
  - Total: $10,000 and .3 BTC
4.
  - Upfront payment of $14,000 (or BTC equivalent) for September - December work
  - It remains 25% for each member


### 2019.12.30
#### Charging Elite
  - 12.12 Signals sent to ATTA elite
  - 12.27 Date of addition of signals to ATTA plebes


### 2020.01.11
#### Actionable steps to deploy fx-signal
  (X) Add oanda data to peter-signal
  (X) Replace local TAcharts with TAcharts module
  (X) Run code to send `TEST` signals
  (X) Validate last signal sent from wc/atta by sending to test
  (X) Create signals for one ticker with no custom logic
  (X) Analyze distribution of trade size and determine which outliers to remove
  (X) Integrate custom trade requirements with basic signals
  (X) Determine TP code
  ( ) Decision tree model for feature importance
  ( ) Add custom logic to algorithm
  ( ) Move code from py to crypto (And fix all file references)

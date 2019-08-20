### 2019.08.08

- Figure out setting TP
  - TP1:
    - .5 * SL
  - TP2:
    - SL
    - Adjust SL to buy-in price
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
  - TP1: (10,100 - 10,000) * 25% + (9,800 - 10,000) * 75% = __- \$125__
  - TP2: (10,100 - 10,000) * 25% + (10,200 - 10,000) * 25% = __+ \$75__
  - TP3: (10,100 - 10,000) * 25% + (10,200 - 10,000) * 25% + (10,400 - 10,000) * 25% = __+ \$175__
  - TP4: (10,100 - 10,000) * 25% + (10,200 - 10,000) * 25% + (10,400 - 10,000) * 25%  + (10,600s - 10,000) * 25% = __+ \$325__

### Risk vs. Reward
risk = 200 + 125 = __$325__
reward = 75 + 175 + 325 = __$575__
reward/risk = 575 / 325 = __1.76923__

### Profit compared to starting SL (\$200)
  - TP0: -200 / 200 = __- 1__
  - TP1: 125 / 200 =  __- 5/8__
  - TP2: 75 / 200 = __+ 3/8__
  - TP3: 175 / 200 = __+ 7/8__
  - TP4: 325 / 200 = __+ 13/8__

- Calculating TP
  - 0: -(100% * SL_pct)
  - TP1: (25% * SL_pct/2) - (75% * SL_pct)
  - TP2: (25% * SL_pct/2) + (25% * SL_pct) - (50% * sl_pct)
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
  - TP1: (10,100 - 10,000) * 40% + (9,800 - 10,000) * 60% = __- \$80__
  - TP2: (10,100 - 10,000) * 40% + (10,200 - 10,000) * 20% = __+ \$80__
  - TP3: (10,100 - 10,000) * 40% + (10,200 - 10,000) * 20% + (10,400 - 10,000) * 20% = __+ \$160__
  - TP4: (10,100 - 10,000) * 40% + (10,200 - 10,000) * 20% + (10,400 - 10,000) * 20%  + (10,600 - 10,000) * 20% = __+ \$280__

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

TP Example
- Buy 1 BTC @ $10,000
- SL = $9,800

TP Levels:
  - TP0 (SL): $9,800
  - TP1: $10,100
  - TP2: $10,200
  - TP3: $10,400
  - TP4: $10,600

Profit Levels:
  - TP0: ($9.8k - $10k) * 100% = -$200
  - TP1: ($10.1k - $10k) * 25% + ($9.8k - $10k) * 75% = -$125
  - TP2: ($10.1k - $10k) * 25% + ($10.2k - $10k) * 25% = +$75
  - TP3: ($10.1k - $10k) * 25% + ($10.2k - $10k) * 25% + ($10.4k - $10k) * 25% = +$175
  - TP4: ($10.1k - $10k) * 25% + ($10.2k - $10k) * 25% + ($10.4k - $10k) * 25%  + ($10.6k - $10k) * 25% = +$275

risk = 200 + 125
reward = 75 + 175 + 275
reward/risk = 1.615384

- SL_pct = (purchase_price - SL) / purchase_price
Profit Levels (%)
  - TP0: -SL_pct
  - TP1: -SL_pct * (5/8)
  - TP2: SL_pct * (3/8)
  - TP3: SL_pct * (7/8)
  - TP4: SL_pct * (11/8)


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

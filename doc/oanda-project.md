### 2020.01.11
#### Actionable steps to deploy fx-signal
- [x] Add oanda data to peter-signal
- [x] Replace local TAcharts with TAcharts module
- [x] Validate last signal sent from wc/atta by sending to test
- [x] Create signals for one ticker with no custom logic
- [x] Analyze distribution of trade size and determine which outliers to remove
- [x] Integrate custom trade requirements with basic signals
- [x] Determine TP code
- [x] Calculate profit
- [x] Copy over oanda py files from fx-signal

### 2020.01.13
#### To-Do
- [ ] Fetch recent prices on demo account
- [ ] Send basic trade on demo account
- [ ] Research FX-choice
- [ ] Run code to send test signals in fx telegram group
- [ ] Backtest
    - [ ] 1. Loop through candle volatility parameters
    - [ ] 2. For each set of parameters:
        - [ ] a. Return absolute return for each set of parameters
        - [ ] b. Return compounded return for each set of parameters
    - [ ] 3. Decision tree model for feature importance

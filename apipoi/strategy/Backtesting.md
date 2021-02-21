## Automatic Backtest system
#### Generating profile of trading pair
In `backtest.py`, function `generate_history()`  can be used to fetch kline data of trading pair with indicator that is essential for MACD strategy.
The function will generate data as `.csv` file which compatible to use with automatic backtest system.

#### Testing MACD strategy
In `backtest.py`, there are two option for strategy of backtesting
* `auto_paper_trade_macd_tradition()` will buy cumulatively and close all opening position once received sell signal,
take profit and cut loss is determined by latest entry position
* `auto_paper_trade_macd_tradition_individual()` also behave the same way, but will determine take profit and cutloss on individual entry position

The function will retrive file that is generated from `generate_history()` and simulate trading follow MACD strategy
* This function has following option for determining Take profit and Cut loss
```python 
fix_takeprofit=True   # Take profit is determined by tp_percent (fixed value)
fix_takeprofit=False  # Take profit is determined by signal from MACD strategy

fix_cutloss=True      # Cut loss is determined by cl_percent (fixed value)
fix_cutloss=False     # Cut loss is determined by signal from MACD strategy

normalize=True        # Change unit of income into percent
```

#### Test MACD strategy with market data of last year
In `backtest.py`, function `past_performance_macd_tradition()` will generate data of each month in last year and conduct backtest.
The function will generate income profile of each month as `.png` file

## Example
#### Generate ETHBUSD data with 5 minute timestep since 60 days ago
```python
generate_history('ETHBUSD', '5m', day_ago=60, until_now=True)
```
#### Generate ETHBUSD data with 5 minute timestep from 1 Sep, 2020 to 31 Oct, 2020
```python
generate_history('ETHBUSD', '5m', date_start='1 Sep, 2020', date_end='31 Oct, 2020', until_now=True)
```
#### Backtest ETHBUSD data with 5 minute timestep since 60 days ago and plot cumulative income graph
```python
import matplotlib.pyplot as plt
from apipoi.strategy import backtest

index, long_entry, close_signal,\
       income, gross_income, fee,\
       gross_fee = backtest.auto_paper_trade_macd_tradition('ETHBUSD', '5m',
                                                            tp_percent = 0.02, cl_percent = 0.01,
                                                            fix_takeprofit=True, fix_cutloss=True,
                                                            normalize=True)

plt.plot(gross_income, '--k', lw=1, label='Income')
plt.plot(gross_fee, 'or', markersize=3, label='Income - Fee')
plt.legend(loc='best')
plt.show()
```

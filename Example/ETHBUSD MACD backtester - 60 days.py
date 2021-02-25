import time

import numpy as np
import matplotlib.pyplot as plt
from apipoi.strategy import backtest

minute = 5
time_step = '{}m'.format(minute)
# valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M

symbol_pair = 'ETHBUSD'
deci = 2    # decimal point

# If historical file is alreay existed, this line is unnecessary
history = backtest.generate_history(symbol_pair, time_step,
                                    day_ago=60, until_now=True)

index, long_entry, close_signal,\
       income, gross_income, fee,\
       gross_fee = backtest.auto_paper_trade_macd_tradition_individual(symbol_pair, time_step,
                                                            tp_percent = 0.08, cl_percent = 0.16,
                                                            fix_takeprofit=True, fix_cutloss=True,
                                                            normalize=True)

plt.plot(income, '-g', alpha=0.6, lw=1)
plt.plot(fee, '--b', alpha=0.6, lw=1)
plt.plot(gross_income, '--k', lw=1)
plt.plot(gross_fee, 'or', markersize=3)
plt.plot(np.zeros(len(fee)), '-y')
plt.show()

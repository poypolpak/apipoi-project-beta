import time

import numpy as np
import matplotlib.pyplot as plt
from apipoi.strategy import backtest

minute = 5
time_step = '{}m'.format(minute)
# valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M

symbol_pair = 'ETHBUSD'
deci = 2    # decimal point

backtest.past_performance_macd_tradition(symbol_pair, time_step,
                                         tp=0.08, cl=0.08,
                                         fix_tp=True, fix_cl=True,
                                         normal=True, indi=True)
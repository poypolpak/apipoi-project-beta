import time

#from apipoi.api_key import test_net, client_test_net
from apipoi.strategy import macd
from apipoi.calculation import entry
import apipoi.retriever.updater as upd

minute = 5
time_step = '{}m'.format(minute)
# valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M

symbol_pair = 'ETHBUSD'
deci = 2    # decimal point

# Eternal loop
while True:    
    obj = time.localtime()    
    if obj[4] % minute == 0:
        try: 
            data_array = upd.updating_price(symbol_pair, time_step, deci)
            
            entry_long, close_long = macd.macd_tradition_strategy(data_array)
            
            entry.position(symbol_pair, time_step, entry_long, close_long)
            time_2 = time.localtime()
            t1 = obj[5]
            t2 = time_2[5]
            t_lag = t2 - t1
            time.sleep(60 - t_lag)

        except Exception as e:
            print('Something went wrong at {}H {}m'.format(obj[3], obj[4]))
            print(type(e), type(e).__qualname__)
            
    time.sleep(60)

import pandas as pd
import btalib

from apipoi.api_key import *

def price_history(symbol_pair, time_step):

    client = client_test_net()

    if time_step == '5m':
        klines = client.get_historical_klines(symbol_pair, Client.KLINE_INTERVAL_5MINUTE, "2 day ago UTC")
    elif time_step == '15m':
        klines = client.get_historical_klines(symbol_pair, Client.KLINE_INTERVAL_15MINUTE, "6 day ago UTC")
    elif time_step == '30m':
        klines = client.get_historical_klines(symbol_pair, Client.KLINE_INTERVAL_30MINUTE, "12 day ago UTC")
    else:
        klines = client.get_historical_klines(symbol_pair, Client.KLINE_INTERVAL_1HOUR, "24 day ago UTC")
#   Remove unnecessary data
    for line in klines:
        del line[6:]
#   Generate csv file of RAW data
    df1 = pd.DataFrame(klines, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df1.set_index('date', inplace=True)
    df1.to_csv('{}_history_{}.csv'.format(symbol_pair, time_step))
#   Prepare to calculate indicator
    df = pd.read_csv('{}_history_{}.csv'.format(symbol_pair, time_step), index_col=0)
    df.index = pd.to_datetime(df.index, unit='ms') + pd.DateOffset(hours=7)
#   Average of high-low *note: is high-low-close better?
    df['avg'] = (df['high'] + df['low'])/2
#   Calculate moving average using Pandas
    df['50ma'] = df.close.rolling(50).mean()
    df['200ma'] = df.close.rolling(200).mean() 
#   VWAP
    df['vwap'] = 0
    volume = df['volume']
    high = df['high']
    low = df['low']
    close = df['close']
    typical_price = (high + low + close) / 3
    for i in range(len(df)):
        if df.index.hour[i] == 23 and df.index.minute[i] == 0:
            df.loc[i: , 'vwap'] = (volume[i:] * typical_price[i:]).cumsum() / volume[i:].cumsum()
#   EMA
    ema200 = btalib.ema(df.close, period=200)
#   MACD
    macd = btalib.macd(df.close, pfast=12, pslow=26, psignal=9)

    df = df.join([ema200.df, macd.df])
#   Export RAW calculated file
    df.to_csv('{}_indicator_{}.csv'.format(symbol_pair, time_step))
#   Remove blank data from calculated file
    df_plot = df[199:-1]

    df_plot.to_csv('{}_indicator_cutted_{}.csv'.format(symbol_pair, time_step))
    return df_plot

def updating_price(symbol_pair, time_step, deci):

    stat = price_history(symbol_pair, time_step)

    last_three = stat.tail(3)
    lt_short = last_three.drop(['open', 'close', 'high', 'low', 'volume', '50ma'], axis = 1)
    
    close_array = last_three['close'].values
    avg_array = last_three['avg'].values
    macd_array = last_three['macd'].values
    signal_array = last_three['signal'].values
    histogram_array = last_three['histogram'].values
    ema_array = last_three['ema'].values
    ma_50_array = last_three['50ma'].values
    ma_200_array = last_three['200ma'].values
    vwap_array = last_three['vwap'].values
    print('pair: {}'.format(symbol_pair))
    print(lt_short.round(deci))

    return [close_array, avg_array, macd_array, signal_array, histogram_array, \
           ema_array, ma_50_array, ma_200_array, vwap_array]

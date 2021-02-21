import time
import btalib
import pandas as pd
import numpy as np

from apipoi.api_key import *
from apipoi.strategy import macd

import matplotlib.pyplot as plt

def generate_history(symbol_pair, time_step, 
                     day_ago=None, date_start=None, date_end=None, until_now=True):
    day_ago = str(day_ago)

    client = client_test_net()

    if until_now:
        klines = client.get_historical_klines(symbol_pair, time_step, '{} day ago UTC'.format(day_ago))
    
    else:
        klines = client.get_historical_klines(symbol_pair, time_step, date_start, date_end)        

    for line in klines:
        del line[6:]
#   Generate csv file of RAW data
    df1 = pd.DataFrame(klines, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df1.set_index('date', inplace=True)
    df1.to_csv('{}_long_history_{}.csv'.format(symbol_pair, time_step))
#   Prepare to calculate indicator
    df = pd.read_csv('{}_long_history_{}.csv'.format(symbol_pair, time_step), index_col=0)
    df.index = pd.to_datetime(df.index, unit='ms') + pd.DateOffset(hours=7)
#   Average of high-low *note: is close-open better?
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
    df.to_csv('{}_history_indicator_{}.csv'.format(symbol_pair, time_step))
#   Remove blank data from calculated file
    df_plot = df[199:-1]

    df_plot.to_csv('{}_history_indicator_cutted_{}.csv'.format(symbol_pair, time_step))
    return df_plot

def auto_paper_trade_macd_tradition(symbol_pair, time_step, tp_percent, cl_percent,
                                    fix_takeprofit=True, fix_cutloss=True,
                                    normalize=True):
    '''
    -----Automatic backtesting system-----
    The algorithm enter position with buying signal from MACD and will
    buy cumulatively until sell signal is given.
    Once received sell signal, Algorithm will close all opening position.
    
    *note: In this Algorithm, take profit and stop lost is updated accord to
    latest entry signal, not individual entry position.
    '''
    cut_loss = -1
    take_profit = 1e8

    tp = 1 + tp_percent
    cl = 1 - cl_percent

    df = pd.read_csv('{}_history_indicator_cutted_{}.csv'.format(symbol_pair, time_step), index_col=0)

    store = np.zeros(len(df.index))

    close_array = df.close.values
    avg_array = df.avg.values
    macd_array = df.macd.values
    signal_array = df.signal.values
    histogram_array = df.histogram.values
    ema_array = df.ema.values
    ma_50_array = df['50ma'].values
    ma_200_array = df['200ma'].values
    vwap_array = df.vwap.values

    for i in range(len(df.index)-2):
        if i > 0:

            close_array_i = close_array[i-1:i+2]
            avg_array_i = avg_array[i-1:i+2]
            macd_array_i = macd_array[i-1:i+2]
            signal_array_i = signal_array[i-1:i+2]
            histogram_array_i = histogram_array[i-1:i+2]
            ema_array_i = ema_array[i-1:i+2]
            ma_50_array_i = ma_50_array[i-1:i+2]
            ma_200_array_i = ma_200_array[i-1:i+2]
            vwap_array_i = vwap_array[i-1:i+2]

            data_array = [close_array_i, avg_array_i, macd_array_i, signal_array_i, histogram_array_i,
                          ema_array_i, ma_50_array_i, ma_200_array_i, vwap_array_i]

            entry_long, close_long = macd.macd_tradition_strategy_only(data_array)

#           Buy position
            if entry_long == True:
                store[i+2] = 1
                cut_loss = avg_array[i+2] * cl
                take_profit = avg_array[i+2] * tp
           
#           Sell position                
            if fix_takeprofit == True:
                if fix_cutloss == True:
                    if close_array[i] > take_profit or close_array[i] < cut_loss:
                        store[i+2] = -1
                if fix_cutloss == False:
                    if close_array[i] > take_profit or close_array[i] < ma_200_array[i]:
                        store[i+2] = -1
            if fix_takeprofit == False:
                if fix_cutloss == True:
                    if close_long == True or close_array[i] < cut_loss:
                        store[i+2] = -1
                if fix_cutloss == False:
                    if close_long == True or close_array[i] < ma_200_array[i]:
                        store[i+2] = -1            
        
    long_entry = np.where(store==1)[0]
    long_close = np.where(store==-1)[0]

    close_signal = []

    for i in range(len(long_entry)):
        for j in range(len(long_close)):
            if long_entry[i] < long_close[j]:
                close_signal += [long_close[j]]
                break
    close_signal = np.asarray(close_signal)
    
    if len(close_signal) != len(long_entry):
        long_entry = long_entry[0:len(close_signal)]
        
    buying = np.asarray([x for x in avg_array[long_entry]])
    selling = np.asarray([y for y in avg_array[close_signal]])
#   Fee
    buy_fee = buying * 0.001
    sell_fee = selling * 0.001
    fee = buy_fee + sell_fee
    
    gross_buy_fee = buying + buy_fee
    gross_sell_fee = selling - sell_fee

    if normalize:
        income = ((selling - buying) / buying) * 100
        income_fee = ((gross_sell_fee - gross_buy_fee) / gross_buy_fee) * 100

        gross_income = np.cumsum(income)
        gross_income_fee = np.cumsum(income_fee)
    else:
        income = selling - buying
        income_fee = gross_sell_fee - gross_buy_fee

        gross_income = np.cumsum(income)
        gross_income_fee = np.cumsum(income_fee)

    return df.index, long_entry, close_signal, income, gross_income, income_fee, gross_income_fee

def auto_paper_trade_macd_tradition_individual(symbol_pair, time_step, tp_percent, cl_percent,
                                        fix_takeprofit=True, fix_cutloss=True,
                                        normalize=True):
    '''
    -----Automatic backtesting system-----
    The algorithm enter position with buying signal from MACD and will
    buy cumulatively until sell signal is given.
    Once received sell signal, Algorithm will close some opening position.
    
    *note: In this Algorithm, take profit and stop lost is
    depend on individual entry position.
    '''
    cut_loss = -1
    take_profit = 1e8

    tp = 1 + tp_percent
    cl = 1 - cl_percent
    
    tp_array = []
    cl_array = []

    df = pd.read_csv('{}_history_indicator_cutted_{}.csv'.format(symbol_pair, time_step), index_col=0)

    store = np.zeros(len(df.index))

    close_array = df.close.values
    avg_array = df.avg.values
    macd_array = df.macd.values
    signal_array = df.signal.values
    histogram_array = df.histogram.values
    ema_array = df.ema.values
    ma_50_array = df['50ma'].values
    ma_200_array = df['200ma'].values
    vwap_array = df.vwap.values

    for i in range(len(df.index)-2):
        if i > 0:

            close_array_i = close_array[i-1:i+2]
            avg_array_i = avg_array[i-1:i+2]
            macd_array_i = macd_array[i-1:i+2]
            signal_array_i = signal_array[i-1:i+2]
            histogram_array_i = histogram_array[i-1:i+2]
            ema_array_i = ema_array[i-1:i+2]
            ma_50_array_i = ma_50_array[i-1:i+2]
            ma_200_array_i = ma_200_array[i-1:i+2]
            vwap_array_i = vwap_array[i-1:i+2]

            data_array = [close_array_i, avg_array_i, macd_array_i, signal_array_i, histogram_array_i,
                          ema_array_i, ma_50_array_i, ma_200_array_i, vwap_array_i]

            entry_long, close_long = macd.macd_tradition_strategy_only(data_array)

#           Buy position
            if entry_long == True:
                store[i+2] = 1
                cut_loss = avg_array[i+2] * cl
                take_profit = avg_array[i+2] * tp
                
                tp_array += [take_profit]
                cl_array += [cut_loss]
                
    long_entry = np.where(store==1)[0]
    
    for j in range(len(tp_array)):
        take_profit = tp_array[j]
        cut_loss = cl_array[j]
        for i in range(long_entry[j], len(df.index)):           
#       Sell position                
            if fix_takeprofit == True:
                if fix_cutloss == True:
                    if close_array[i] > take_profit or close_array[i] < cut_loss:
                        store[i] = -1
                        break
                if fix_cutloss == False:
                    if close_array[i] > take_profit or close_array[i] < ma_200_array[i]:
                        store[i] = -1
                        break
            if fix_takeprofit == False:
                if fix_cutloss == True:
                    if close_long == True or close_array[i] < cut_loss:
                        store[i] = -1
                        break
                if fix_cutloss == False:
                    if close_long == True or close_array[i] < ma_200_array[i]:
                        store[i] = -1
                        break
            
    long_close = np.where(store==-1)[0]

    close_signal = []

    for i in range(len(long_entry)):
        for j in range(len(long_close)):
            if long_entry[i] < long_close[j]:
                close_signal += [long_close[j]]
                break
    close_signal = np.asarray(close_signal)
    
    if len(close_signal) != len(long_entry):
        long_entry = long_entry[0:len(close_signal)]
        
    buying = np.asarray([x for x in avg_array[long_entry]])
    selling = np.asarray([y for y in avg_array[close_signal]])
#   Fee
    buy_fee = buying * 0.001
    sell_fee = selling * 0.001
    fee = buy_fee + sell_fee
    
    gross_buy_fee = buying + buy_fee
    gross_sell_fee = selling - sell_fee

    if normalize:
        income = ((selling - buying) / buying) * 100
        income_fee = ((gross_sell_fee - gross_buy_fee) / gross_buy_fee) * 100

        gross_income = np.cumsum(income)
        gross_income_fee = np.cumsum(income_fee)
    else:
        income = selling - buying
        income_fee = gross_sell_fee - gross_buy_fee

        gross_income = np.cumsum(income)
        gross_income_fee = np.cumsum(income_fee)

    return df.index, long_entry, close_signal, income, gross_income, income_fee, gross_income_fee

def past_performance_macd_tradition(symbol_pair, time_step,
                                    tp, cl,
                                    fix_tp=True, fix_cl=True,
                                    normal=True):

    month = ['Jan','Feb','Mar', 'Apr','May','Jun',
             'Jul','Aug','Sep','Oct','Nov','Dec']
    end_d = ['31','28','31','30','31','30',
             '31','31','30','31','30','31']

    date_start_list = ['1 {}, 2020'.format(m) for m in month]
    date_end_list = ['{} {}, 2020'.format(end_d[d], m) for d, m in enumerate(month)]

    for i, j in enumerate(date_end_list):
        date_start = date_start_list[i]

        try:
            history = generate_history(symbol_pair, time_step,
                                       date_start=date_start, date_end=j,
                                       until_now=False)
        except:
            print('Something is wrong in {}, no data or bad connection'.format(date_start))
            continue
        try:
            index, long_entry, close_signal,\
                   income, gross_income,\
                   fee, gross_fee = auto_paper_trade_macd_tradition(symbol_pair, time_step,
                                                                    tp_percent=tp, cl_percent=cl,
                                                                    fix_takeprofit=fix_tp, fix_cutloss=fix_cl,
                                                                    normalize=normal)

            fig = plt.figure(figsize=(12, 6))
            ax1 = fig.add_subplot(121)
            plt.plot(income, 'k--', label='Income')
            plt.plot(fee, 'b-', label='Profit')
            plt.legend(loc='upper left')
            plt.xlim(0, len(income))
            plt.title('Income from each position')
            ax1.set_xlabel('Trade')
            ax1.set_ylabel('Normalized Income')
            

            ax2 = fig.add_subplot(122)
            plt.plot(gross_income, 'k--', label='Gross Income')
            plt.plot(gross_fee, 'r-', label='Gross Profit')
            plt.legend(loc='upper left')
            plt.xlim(0, len(gross_income))
            plt.title('Gross Income')
            ax2.set_xlabel('Trade')
            ax2.set_ylabel('Normalized Income')
            
            if i < 9:
                plt.savefig('{}_backtest_{}_ftp={}_fcl={}_tp{}_cl{}_in_0{}_{}.png'.format(symbol_pair, time_step,
                                                                                          fix_tp, fix_cl,
                                                                                          tp*100, cl*100,
                                                                                          i+1, date_start), dpi=400)
            else:
                plt.savefig('{}_backtest_{}_ftp={}_fcl={}_tp{}_cl{}_in_{}_{}.png'.format(symbol_pair, time_step,
                                                                                         fix_tp, fix_cl,
                                                                                         tp*100, cl*100,
                                                                                         i+1, date_start), dpi=400)
        except:
            print('Something is wrong in {}, no position taken'.format(date_start))

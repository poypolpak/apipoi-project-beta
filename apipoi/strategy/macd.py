import time

def macd_tradition_strategy(data_array):
    '''
    ----- The MACD classic cross-over strategy -----
    Long position:
        Buy when cross-over happend below zero, price moving above 200ma
        close position when cross-over happend above zero

    Short position:
        Sell when cross-over happen above zero, price moving below 200ma
        close position when cross-over happend below zero
    '''
    close_array = data_array[0]
    avg_array = data_array[1]
    macd_array = data_array[2]
    signal_array = data_array[3]
    histogram_array = data_array[4]
    ema_array = data_array[5]
    ma_50_array = data_array[6]
    ma_200_array = data_array[7]
    vwap_array = data_array[8]
    
    au_line = '-------------------------'
    g_line = '*************************'

    entry_long = None
    close_long = None

#   Golden cross up trend
    if ma_50_array[-1] > ma_200_array[-1] and ma_50_array[-2] > ma_200_array[-2]:
        print(au_line)
        print('golden cross: up trend\n' + au_line)
#   Golden cross down trend      
    if ma_50_array[-1] < ma_200_array[-1] and ma_50_array[-2] < ma_200_array[-2]:
        print(au_line)
        print('golden cross: down trend\n' + au_line)

# Buy signal, enter long position
    if avg_array[-1] > ema_array[-1] and avg_array[-2] > ema_array[-2] \
       and avg_array[-1] > ma_200_array[-1] and avg_array[-2] > ma_200_array[-2]:
        print(au_line + '\nma: up trend')
        print(au_line)

#       Cross-over up
        if histogram_array[-1] > 0 and histogram_array[-2] < 0 and histogram_array[-1] > histogram_array[-2]:

#           Cross-over below zero
            if macd_array[-2] < 0 and signal_array[-2] < 0:
                print('Buy signal (long, MACD)\n' + au_line + '\n')
                entry_long = True

#       Cross-over down
        if histogram_array[-1] < 0 and histogram_array[-2] > 0 and histogram_array[-1] < histogram_array[-2] \
           and macd_array[-2] > 0 and signal_array[-2] > 0:
            print('close long position')
            close_long = True
            
# Sell signal, enter short position *note: this api is on spot market
    if avg_array[-1] < ema_array[-1] and avg_array[-2] < ema_array[-2] \
       and avg_array[-1] < ma_200_array[-1] and avg_array[-2] < ma_200_array[-2]:
        print(au_line + '\nma: down trend')
        print(au_line)

#       Cross-over down
        if histogram_array[-1] < 0 and histogram_array[-2] > 0 and histogram_array[-1] < histogram_array[-2]:

#           Cross-over above zero
            if macd_array[-2] > 0 and signal_array[-2] > 0:
                print('Sell signal (short, MACD)')
                entry_long = False

#       Cross-over up
        if histogram_array[-1] > 0 and histogram_array[-2] < 0 and histogram_array[-1] > histogram_array[-2] \
           and macd_array[-2] < 0 and signal_array[-2] < 0:
            print('close short position')
            close_long = False

    print(g_line)
    return entry_long, close_long
	
def macd_tradition_strategy_only(data_array):
    '''
    ----- The MACD classic cross-over strategy value only -----
    '''
    close_array = data_array[0]
    avg_array = data_array[1]
    macd_array = data_array[2]
    signal_array = data_array[3]
    histogram_array = data_array[4]
    ema_array = data_array[5]
    ma_50_array = data_array[6]
    ma_200_array = data_array[7]
    vwap_array = data_array[8]
    
    au_line = '-------------------------'
    g_line = '*************************'

    entry_long = None
    close_long = None

# Buy signal, enter long position
    if avg_array[-1] > ema_array[-1] and avg_array[-2] > ema_array[-2] \
       and avg_array[-1] > ma_200_array[-1] and avg_array[-2] > ma_200_array[-2]:

#       Cross-over up
        if histogram_array[-1] > 0 and histogram_array[-2] < 0 and histogram_array[-1] > histogram_array[-2]:

#           Cross-over below zero
            if macd_array[-2] < 0 and signal_array[-2] < 0:
                entry_long = True

#       Cross-over down
        if histogram_array[-1] < 0 and histogram_array[-2] > 0 and histogram_array[-1] < histogram_array[-2] \
           and macd_array[-2] > 0 and signal_array[-2] > 0:
            close_long = True
            
# Sell signal, enter short position *note: this api is on spot market
    if avg_array[-1] < ema_array[-1] and avg_array[-2] < ema_array[-2] \
       and avg_array[-1] < ma_200_array[-1] and avg_array[-2] < ma_200_array[-2]:

#       Cross-over down
        if histogram_array[-1] < 0 and histogram_array[-2] > 0 and histogram_array[-1] < histogram_array[-2]:

#           Cross-over above zero
            if macd_array[-2] > 0 and signal_array[-2] > 0:
                entry_long = False

#       Cross-over up
        if histogram_array[-1] > 0 and histogram_array[-2] < 0 and histogram_array[-1] > histogram_array[-2] \
           and macd_array[-2] < 0 and signal_array[-2] < 0:
            close_long = False

    return entry_long, close_long

def macd_histogram_strategy(data_array):
    '''
    ----- The MACD modified strategy No.1 -----
    Long position:
        Buy when histogram is reversing while MACD is lower than about -6.6883 (or some value)
        close position when histogram is reverse again

    '''
    close_array = data_array[0]
    avg_array = data_array[1]
    macd_array = data_array[2]
    signal_array = data_array[3]
    histogram_array = data_array[4]
    ema_array = data_array[5]
    ma_50_array = data_array[6]
    ma_200_array = data_array[7]
    vwap_array = data_array[8]
    
    au_line = '-------------------------'
    g_line = '*************************'

    entry_long = None
    close_long = None

def macd_custom_strategy(data_array):
    '''
    ----- The MACD custom strategy -----

    '''
    close_array = data_array[0]
    avg_array = data_array[1]
    macd_array = data_array[2]
    signal_array = data_array[3]
    histogram_array = data_array[4]
    ema_array = data_array[5]
    ma_50_array = data_array[6]
    ma_200_array = data_array[7]
    vwap_array = data_array[8]
    
    au_line = '-------------------------'
    g_line = '*************************'

    entry_long = None
    close_long = None

    if macd_array [-1] < 0:
        print('')
    if signal_array[-1] < 0:
        print('')
    if histogram_array[-1] / histogram_array[-2] >= 1.01:
        print('')

import time

from apipoi.api_key import client_test_net

def current_price(symbol_pair):
    client = client_test_net()    
    price_dict = client.get_avg_price(symbol=symbol_pair)
    return float(price_dict['price'])
    
def position(symbol_pair, time_step, entry_long, close_long):
    
    client = client_test_net()

    take_profit_percent = 0.02      # tp
    cut_loss_percent = 0.01         # sl
# Calculate tp/sl
# Long position
    take_profit_long = 1 + take_profit_percent
    cut_loss_long = 1 - cut_loss_percent
# Short position
    take_profit_short = 1 - take_profit_percent
    cut_loss_short = 1 + cut_loss_percent

    au_line = '-------------------------'
    g_line = '*************************'
    
    obj = time.localtime()

    if entry_long == True:
        price_dict = client.get_avg_price(symbol=symbol_pair)
        price_enter = float(price_dict['price'])
        l_take_profit = price_enter * take_profit_long
        l_cut_loss = price_enter * cut_loss_long
        print('Price enter: {}\n tp: {}\n cl: {}'.format(price_enter, l_take_profit, l_cut_loss))            
        print(au_line)
        
        with open('{}_backtest_action_log_{}.txt'.format(symbol_pair, time_step), 'a+') as f:
            f.write('\nTime: Month{} D{}, {}H {}m\n'.format(obj[1], obj[2], obj[3], obj[4]))
            f.write('{}\nPrice enter long: {}\ntp: {}\ncl: {}\n{}\n'.format(au_line,
                                                                            price_enter,
                                                                            l_take_profit,
                                                                            l_cut_loss,
                                                                            au_line))
    if entry_long == False:
        price_dict = client.get_avg_price(symbol=symbol_pair)
        price_enter = float(price_dict['price'])
        s_take_profit = price_enter * take_profit_short
        s_cut_loss = price_enter * cut_loss_short
        print('Price enter: {}\n tp: {}\n cl: {}'.format(price_enter, s_take_profit, s_cut_loss))            
        print(au_line)
        
        with open('{}_backtest_action_log_{}.txt'.format(symbol_pair, time_step), 'a+') as f:
            f.write('\nTime: Month{} D{}, {}H {}m\n'.format(obj[1], obj[2], obj[3], obj[4]))
            f.write('{}\nPrice enter short: {}\ntp: {}\ncl: {}\n{}\n'.format(au_line,
                                                                            price_enter,
                                                                            s_take_profit,
                                                                            s_cut_loss,
                                                                            au_line))

    if close_long == True:
        price_dict = client.get_avg_price(symbol=symbol_pair)
        price_close = float(price_dict['price'])
        with open('{}_backtest_action_log_{}.txt'.format(symbol_pair, time_step), 'a+') as f:
            f.write('\nTime: Month{} D{}, {}H {}m\n'.format(obj[1], obj[2], obj[3], obj[4]))
            f.write('{}\nPrice close long: {}\n{}\n'.format(au_line, price_close, au_line))

    if close_long == False:
        price_dict = client.get_avg_price(symbol=symbol_pair)
        price_close = float(price_dict['price'])
        with open('{}_backtest_action_log_{}.txt'.format(symbol_pair, time_step), 'a+') as f:
            f.write('\nTime: Month{} D{}, {}H {}m\n'.format(obj[1], obj[2], obj[3], obj[4]))
            f.write('{}\nPrice close short: {}\n{}\n'.format(au_line, price_close, au_line))

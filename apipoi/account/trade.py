import json

from apipoi.api_key import *
from binance.enums import *

def create_order_limit_buy(client, symbol_pair, quantity, price):
    order = client.create_order(
        symbol = symbol_pair,
        side = SIDE_BUY,
        type = ORDER_TYPE_LIMIT,
        timeInForce = TIME_IN_FORCE_GTC,
        quantity = quantity,
        price = price)
    print(json.dumps(order, indent = 4))
    return order

def create_order_market_buy(client, symbol_pair, quantity):
    order = client.create_order(
        symbol = symbol_pair,
        side = SIDE_BUY,
        type = ORDER_TYPE_MARKET,
        quantity = quantity)
    print(json.dumps(order, indent = 4))
    return order

def create_order_limit_sell(client, symbol_pair, quantity, price):
    order = client.create_order(
        symbol = symbol_pair,
        side = SIDE_SELL,
        type = ORDER_TYPE_LIMIT,
        timeInForce = TIME_IN_FORCE_GTC,
        quantity = quantity,
        price = price)
    print(json.dumps(order, indent = 4))
    return order

def create_order_market_sell(client, symbol_pair, quantity):
    order = client.create_order(
        symbol = symbol_pair,
        side = SIDE_SELL,
        type = ORDER_TYPE_MARKET,
        quantity = quantity)
    print(json.dumps(order, indent = 4))
    return order

def create_oco_buy(client, symbol_pair, quantity, price, stop_p, stop_lim_p):
    order = client.create_oco_order(
        symbol = symbol_pair,
        side = SIDE_BUY,        
        quantity = quantity,        
        price = price,
        stopPrice = stop_p,
        stopLimitPrice = stop_lim_p,
        stopLimitTimeInForce = TIME_IN_FORCE_GTC)
    print(json.dumps(order, indent = 4))
    return order

def create_oco_sell(client, symbol_pair, quantity, price, stop_p, stop_lim_p):
    order = client.create_oco_order(
        symbol = symbol_pair,
        side = SIDE_SELL,        
        quantity = quantity,        
        price = price,
        stopPrice = stop_p,
        stopLimitPrice = stop_lim_p,
        stopLimitTimeInForce = TIME_IN_FORCE_GTC)
    print(json.dumps(order, indent = 4))
    return order

'''
to create list:
stop limit order, to test API and order placement system
'''

def open_order(client, symbol_pair):
    orders = client.get_open_orders(symbol = symbol_pair)
    print(json.dumps(orders, indent = 4))
    return orders

def fetch_order(client, symbol_pair, limit):   # View last 10 trade history
    orders = client.get_all_orders(symbol = symbol_pair, limit = limit)
    print(json.dumps(orders, indent = 4))
    return orders

from binance.client import Client

def test_net():
    api_key = 'Input your API Key here'
    api_secret = 'Input your API Secret here'
    return api_key, api_secret

def client_test_net():
    api_key, api_secret = test_net()
    client = Client(api_key, api_secret)
    return client

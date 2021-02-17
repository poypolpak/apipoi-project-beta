from binance.client import Client

def test_net():
    prototype1_key = '58Vy1luWGXy5lTf4oBDc3BRexG1Usmt1JS64NiYTR7nyaaIMUXAUvDcPsXCUzpY6'
    prototype1_secret = 'cwZAGNOEtSNJLgr45TAqLXVOporuYQMyF3X5PRIqsoNHwfS8pwtSQJL9M1iTvbjd'
    key = prototype1_key
    secret = prototype1_secret
    return key, secret

def client_test_net():
    api_key, api_secret = test_net()
    client = Client(api_key, api_secret)
    return client

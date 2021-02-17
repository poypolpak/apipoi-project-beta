## Inputting API Key and API Secret
* The file `api_key.py` is where API Key and API Secret is stored
* Simply input your key into `test_net()` function
* If you only want to study and do research about crypto market, the API key from binance-testnet is a good place to start
* This example also use API key from testnet to collect market data and design trading strategy

```python
def test_net():
    api_key = 'Input your API Key here'
    api_secret = 'Input your API Secret here'
    return api_key, api_secret
```

## Accessing market data and account
* The function `client_test_net()` will be used throughout this code to access market data and do analysis

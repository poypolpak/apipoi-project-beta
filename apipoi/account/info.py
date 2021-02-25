import json

def full_info(client):
    acc_info = client.get_account()     # Get account info
    print(json.dumps(acc_info, indent = 4))
    
def balances_check(client):
    acc_info = client.get_account()     # Get account info
    print(json.dumps(acc_info['balances'], indent = 4))

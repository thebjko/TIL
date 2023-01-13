import requests
from pprint import pprint 

def get_btc_krw():
    order_currency = 'BTC'
    payment_currency = 'KRW'
    url = f'https://api.bithumb.com/public/ticker/{order_currency}_{payment_currency}'

    res = requests.get(url=url).json()
    data = res['data']
    prev_closing_price = data.get('prev_closing_price')
    
    return prev_closing_price
    

if __name__ == '__main__':
    pprint(get_btc_krw())
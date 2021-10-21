import hmac
from datetime import datetime
from hashlib import sha512
from urllib import parse

import requests
from src.settings import (MB_TAPI_ID, MB_TAPI_SECRET, REQUEST_HOST,
                          TRADER_REQUEST_PATH, OrderType, Pair)


class MBTrader:

    def __init__(self):
        self.tapi_id = MB_TAPI_ID
        self.tapi_secret = MB_TAPI_SECRET

    @staticmethod
    def __generate_nonce():
        tapi_nonce = str(int(datetime.now().timestamp()))
        return tapi_nonce

    def post(self, method, params, nome_retorno=''):

        params['tapi_method'] = method
        tapi_nonce = self.__generate_nonce()
        params['tapi_nonce'] = tapi_nonce
        params = parse.urlencode(params)

        params_string = TRADER_REQUEST_PATH + '?' + params
        H = hmac.new(bytearray(self.tapi_secret.encode()), digestmod=sha512)
        H.update(params_string.encode())
        tapi_mac = H.hexdigest()

        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'TAPI-ID': self.tapi_id,
            'TAPI-MAC': tapi_mac
        }

        try:
            response = requests.post(
                "https://{}{}".format(REQUEST_HOST, TRADER_REQUEST_PATH),
                headers=headers,
                data=params
            )

            if response.json()['status_code'] == 100:
                return response.json()
            else:
                print(response.json()['error_message'])
                return response.json()

        except requests.exceptions.RequestException as exc:
            print(f"\nThe Mercado Bitcoin Trade API is not available. Exception: {exc}")

    def get_account_info(self):
        return self.post('get_account_info', params={})

    def make_order(self, order_type: OrderType, coin_pair: Pair, quantity: str, limit_price: str):

        params = {
            'coin_pair': coin_pair.value,
            'quantity': quantity,
            'limit_price': limit_price
        }
        method = f'place_{order_type.value}_order'
        return self.post(method, params, 'order')

    def cancel_order(self, coin_pair: Pair, order_id):

        params = {
            'coin_pair': coin_pair.value,
            'order_id': order_id,
        }
        return self.post('cancel_order', params)


class MBInfo:

    def __init__(self, coin):
        self.coin = coin

    def __request(self, method, params=None):
        url = f'https://www.mercadobitcoin.net/api/{self.coin}/{method}'
        try:
            response = requests.get(url)
            return response
        except requests.exceptions.RequestException:
            print("\nThe Mercado Bitcoin Data API is not available.")

    def ticker(self):
        method = 'ticker'
        return self.__request(method)

    def orderbook(self):
        method = 'orderbook'
        return self.__request(method)

    def get_candles_1h(self, past: int, now: int):
        url = f"https://mobile.mercadobitcoin.com.br/v4/BRL{self.coin}/candle?from={past}&to={now}&precision=1h"
        headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0"}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            print(f"\nThe Mercado Bitcoin Data API is not available for {self.coin} candles.")

import hmac
import json

from http import client
from urllib import parse
from hashlib import sha512
from collections import OrderedDict

from src.config.settings import Pair
from src.config.settings import OrderType
from src.config.settings import TRADER_REQUEST_PATH
from src.config.settings import REQUEST_HOST
from src.config.settings import MB_TAPI_ID
from src.config.settings import MB_TAPI_SECRET


class MB:

    def __init__(self):
        self.tapi_id = MB_TAPI_ID
        self.tapi_secret = MB_TAPI_SECRET

    def post(self, method, params, nome_retorno=''):

        params['tapi_method'] = method
        tapi_nonce = int(time.time()*1000)
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
            conn = client.HTTPSConnection(REQUEST_HOST)
            conn.request("POST", TRADER_REQUEST_PATH, params, headers)

            response = conn.getresponse()
            response = response.read()

            response_json = json.loads(response, object_pairs_hook=OrderedDict)

            if response_json['status_code'] != 100:
                print(response_json['error_message'])

            if nome_retorno and nome_retorno != '':
                return json.dumps(response_json['response_data'][nome_retorno], indent=4)
            else:
                return json.dumps(response_json['response_data'], indent=4)
        finally:
            if conn:
                conn.close()

    def get_account_info(self):
        params = {}
        return self.post('get_account_info', params)

    def buy(self, coin_pair: Pair, quantity: str, limit_price: str):
        return self.make_order(OrderType.BUY, coin_pair, quantity, limit_price)

    def sell(self, coin_pair: Pair, quantity: str, limit_price: str):
        return self.make_order(OrderType.SELL, coin_pair, quantity, limit_price)

    def make_order(self, order_type, coin_pair, quantity, limit_price):

        params = {
            'coin_pair': coin_pair.value,
            'quantity': quantity,
            'limit_price': limit_price
        }
        method = f'place_{order_type.value}_order'
        return self.post(method, params, 'order')

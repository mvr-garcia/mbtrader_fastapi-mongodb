import hmac
import json

from collections import OrderedDict
from datetime import datetime
from hashlib import sha512
from http import client
from urllib import parse, request

from src.config.settings import Pair
from src.config.settings import OrderType
from src.config.settings import TRADER_REQUEST_PATH
from src.config.settings import API_REQUEST_PATH
from src.config.settings import REQUEST_HOST
from src.config.settings import MB_TAPI_ID
from src.config.settings import MB_TAPI_SECRET


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
        return self.post('get_account_info', params={})

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


class MBInfo:

    async def get(self, method, nome_retorno=''):
        req = request.Request('https://'+REQUEST_HOST + API_REQUEST_PATH + method)
        r = request.urlopen(req).read()
        response = json.loads(r.decode('utf-8'), object_pairs_hook=OrderedDict)

        if(nome_retorno and nome_retorno != ''):
            return json.dumps(response[nome_retorno], indent=4)
        else:
            return json.dumps(response, indent=4)

    async def ticker(self):
        '''Retorna as informações do mercado de bitcoin.'''
        return self.get('ticker', 'ticker')

    async def ticker_litecoin(self):
        '''Retorna as informações do mercado de litecoin.'''
        return self.get('ticker_litecoin', 'ticker')

    async def orderbook(self):
        '''Retorna o livro de ofertas do mercado de bitcoin.'''
        return self.get('orderbook')

    async def orderbook_litecoin(self):
        '''Retorna o livro de ofertas do mercado de litecoin.'''
        return self.get('orderbook_litecoin')

from enum import Enum


REQUEST_HOST = 'www.mercadobitcoin.com.br'
TRADER_REQUEST_PATH = '/tapi/v3/'
API_REQUEST_PATH = '/api/'


class Fiat(Enum):
    USD = 'Dolar'
    BRL = 'Reais'


class Coin(Enum):
    BTC = 'Bitcoin'
    ETH = 'Ethereum'


class OrderType(Enum):
    BUY = 'buy'
    SELL = 'sell'

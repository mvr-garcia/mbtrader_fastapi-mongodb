import os
from enum import Enum

MB_TAPI_ID = os.environ["MB_TAPI_ID"]
MB_TAPI_SECRET = os.environ["MB_TAPI_SECRET"]
REQUEST_HOST = 'www.mercadobitcoin.com.br'
TRADER_REQUEST_PATH = '/tapi/v3/'

PORTFOLIO_INVESTMENT_PERCENTAGE = 0.05
MAX_ORDERS_PER_DAY = 6


class Fiat(Enum):
    BRL = 'Reais'


class Coin(Enum):
    BTC = 'Bitcoin'
    ETH = 'Ethereum'


class Pair(Enum):
    BRLBTC = Fiat.BRL.name + Coin.BTC.name
    BRLETH = Fiat.BRL.name + Coin.ETH.name


class OrderType(Enum):
    BUY = 'buy'
    SELL = 'sell'

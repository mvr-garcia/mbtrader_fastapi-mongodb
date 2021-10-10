from enum import Enum


class Fiat(Enum):
    USD = 'Dolar'
    BRL = 'Reais'


class Coin(Enum):
    BTC = 'Bitcoin'
    ETH = 'Ethereum'


class OrderType(Enum):
    BUY = 'bid'
    SELL = 'ask'

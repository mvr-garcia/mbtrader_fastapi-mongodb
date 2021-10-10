from datetime import datetime
from pydantic import BaseModel

from server.config.settings import Fiat
from server.config.settings import Coin
from server.config.settings import OrderType


class Order(BaseModel):

    fiat: str = Fiat.BRL.value
    symbol: str = Coin.BTC.value
    pair: str = f"{Fiat.BRL.name}{Coin.BTC.name}"
    order_type: str = OrderType.BUY.value
    quantity: float
    fee: float
    net_quantity: float
    created: datetime = datetime.now()

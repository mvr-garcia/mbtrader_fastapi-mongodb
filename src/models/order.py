from datetime import datetime
from pydantic import BaseModel

from src.config.settings import Fiat
from src.config.settings import Coin
from src.config.settings import OrderType


class Order(BaseModel):

    fiat: str = Fiat.BRL.value
    symbol: str = Coin.BTC.value
    pair: str = f"{Fiat.BRL.name}{Coin.BTC.name}"
    order_type: str = OrderType.BUY.value
    quantity: float
    fee: float
    net_quantity: float
    created: datetime = datetime.now()

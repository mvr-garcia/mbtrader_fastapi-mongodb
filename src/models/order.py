from datetime import datetime
from pydantic import BaseModel

from src.settings import Fiat
from src.settings import Coin
from src.settings import OrderType


class Order(BaseModel):

    fiat: str = Fiat.BRL.value
    symbol: str = Coin.BTC.value
    pair: str = f"{Fiat.BRL.name}{Coin.BTC.name}"
    order_type: str = OrderType.BUY.value
    quantity: str
    fee: float
    net_quantity: float
    created: str = datetime.now().isoformat()

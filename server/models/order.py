from pydantic import BaseModel


class Order(BaseModel):

    fiat: str
    symbol: str
    pair: str
    order_type: str
    quantity: float
    fee: float
    net_quantity: float
    created_timestamp: int

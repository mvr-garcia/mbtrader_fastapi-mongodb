from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):

    name: str
    email: str
    balance_brl: float = 0
    balance_btc: str = '0'
    balance_eth: str = '0'
    created: datetime = datetime.now()

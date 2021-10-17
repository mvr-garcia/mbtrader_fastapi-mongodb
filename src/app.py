import time
from fastapi import FastAPI

from src.entities.trader import Trader
from src.routes.order import order
from src.routes.user import user
from src.settings import Coin


app = FastAPI()

app.include_router(order)
app.include_router(user)

print("\nInitializing MV AutoTrader")

my_id = "616c979e96b218462c9120ab"

for coin in Coin:
    Trader(my_id, coin.name).take_decision()
    print(f"\nFinish trading for {coin.value} in MV AutoTrader")

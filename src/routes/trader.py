import time
from threading import Thread

from fastapi import APIRouter

from src.settings import Coin
from src.entities.trader import Trader

trader = APIRouter()


@trader.get('/start/')
async def start_trader():
    print("\nInitializing MV AutoTrader")
    global trading
    trading = True
    Thread(target=job).start()
    return {"status": "success"}


@trader.get('/stop/')
async def stop_trader():
    print("\nStoping MV AutoTrader")
    global trading
    trading = False
    Thread(target=job).start()
    return {"status": "success"}


def job():
    global trading
    while trading:
        my_id = "616c979e96b218462c9120ab"
        for coin in Coin:
            Trader(my_id, coin.name).take_decision()
            print(f"\nFinish trading for {coin.value} in MV AutoTrader")

        time.sleep(30)

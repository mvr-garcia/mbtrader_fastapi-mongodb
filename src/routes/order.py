from decimal import Decimal
from fastapi import APIRouter
from datetime import datetime


from src.entities.mercadobitcoin import MBTrader
from src.entities.user import UserMongo
from src.schemas.order import orders_entity
from src.settings import Pair
from src.database.db import DB


order = APIRouter()


@order.get('/order/')
async def list_orders():
    results = DB.trader.order.find()
    serialized = orders_entity(results)
    return serialized


@order.get('/order/{pair}/{order_id}')
async def get_mb_order(pair, order_id):
    response = MBTrader().get_order(Pair[pair], order_id)
    if response["response_data"]["order"]["has_fills"]:
        await manual_transaction(response)
        return "Success"
    return "Transaction hasn't already executed."


async def manual_transaction(response):

    pair = response["response_data"]["order"]["coin_pair"]

    user_instance = UserMongo("616c979e96b218462c9120ab")
    user = user_instance.get()
    limit_price = response["response_data"]["order"]["limit_price"]
    quantity = response["response_data"]["order"]["executed_quantity"]
    fee = response["response_data"]["order"]["fee"]
    net_quantity = Decimal(quantity) - Decimal(fee)
    brl_amount = round(float(net_quantity * Decimal(limit_price)), 2)

    if response["response_data"]["order"]["order_type"] == 2:
        user["balance_brl"] = user["balance_brl"] + brl_amount
        user[f"balance_{pair[3:].lower()}"] = "0"

    elif response["response_data"]["order"]["order_type"] == 1:
        user["balance_brl"] = user["balance_brl"] - brl_amount
        balance = str(Decimal(user[f"balance_{pair[3:].lower()}"]) + net_quantity)
        user[f"balance_{pair[3:].lower()}"] = balance

    user_instance.update(user)
    order = {
        "user_id": user["id"],
        "fiat": "Reais",
        "symbol": "Bitcoin",
        "price": limit_price,
        "pair": pair,
        "order_type": "buy",
        "quantity": quantity,
        "fee": fee,
        "net_quantity": str(net_quantity),
        "created": datetime.now().isoformat()
    }
    DB.trader.order.insert_one(order)

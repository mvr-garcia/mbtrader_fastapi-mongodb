from fastapi import APIRouter

from src.models.order import Order
from src.schemas.order import orders_entity
from src.database.db import DB


order = APIRouter()


@order.get('/order/')
async def list_orders():
    results = DB.trader.order.find()
    serialized = orders_entity(results)
    return serialized


@order.post('/order/')
async def create_order(order: Order):
    DB.trader.order.insert_one(dict(order))
    return list_orders()

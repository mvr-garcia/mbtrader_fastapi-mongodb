from fastapi import APIRouter

from src.models.order import Order
from src.schemas.order import orders_entity
from src.config.db import CONN


order = APIRouter()


@order.get('/')
async def list_orders():
    results = CONN.trader.order.find()
    serialized = orders_entity(results)
    return serialized


@order.post('/')
async def create_order(order: Order):
    CONN.trader.order.insert_one(dict(order))
    return list_orders()

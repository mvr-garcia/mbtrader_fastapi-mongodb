from fastapi import APIRouter

from server.models.order import Order
from server.schemas.order import order_entity, orders_entity
from server.config.db import CONN


order = APIRouter()


@order.get('/')
async def list_orders():
    return orders_entity(CONN.trader.order.find())


@order.post('/')
async def create_order(order: Order):
    CONN.trader.order.insert_one(dict(order))
    return orders_entity(CONN.trader.order.find())

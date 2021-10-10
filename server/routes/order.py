from fastapi import APIRouter

from server.models.order import Order
from server.schemas.order import order_entity, orders_entity
from server.config.db import CONN


order = APIRouter()


@order.get('/')
async def all_orders():
    print(CONN.trader.order.find())
    print(orders_entity(CONN.trader.order.find()))
    return orders_entity(CONN.trader.order.find())

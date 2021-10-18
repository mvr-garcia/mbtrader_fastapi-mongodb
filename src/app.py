from fastapi import FastAPI

from src.routes.order import order
from src.routes.user import user
from src.routes.trader import trader


app = FastAPI()

app.include_router(order)
app.include_router(user)
app.include_router(trader)

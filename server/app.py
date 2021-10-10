from fastapi import FastAPI
from server.routes.order import order


app = FastAPI()

app.include_router(order)

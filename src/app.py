from fastapi import FastAPI
from src.routes.order import order


app = FastAPI()

app.include_router(order)

i = 0

while i < 10:
    print("\nfazendo trade")
    i += 1

from fastapi import FastAPI
from src.routes.order import order
from src.routes.user import user


app = FastAPI()

app.include_router(order)
app.include_router(user)

i = 0

while i < 10:
    print("\nfazendo trade")
    i += 1

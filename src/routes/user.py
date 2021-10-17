from fastapi import APIRouter
from bson import ObjectId

from src.models.user import User
from src.schemas.user import user_entity
from src.schemas.user import users_entity
from src.database.db import DB


user = APIRouter()


@user.get('/user/')
async def list_users():
    results = DB.trader.user.find()
    serialized = users_entity(results)
    return serialized


@user.post('/user/')
async def create_user(user: User):
    DB.trader.user.insert_one(dict(user))
    results = DB.trader.user.find()
    serialized = users_entity(results)
    return serialized


@user.put('/user/{id}')
async def update_user(id, user: User):
    DB.trader.user.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(user)
    })
    serialized = user_entity(DB.trader.user.find_one({"_id": ObjectId(id)}))
    return serialized


@user.patch('/user/{id}/deposit')
async def user_fiat_deposit(id, value: dict):
    user = DB.trader.user.find_one({"_id": ObjectId(id)})
    user = user_entity(user)
    user["balance_brl"] = user["balance_brl"] + value["deposit_value"]
    DB.trader.user.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(user)
    })
    serialized = user_entity(DB.trader.user.find_one({"_id": ObjectId(id)}))
    return serialized


@user.patch('/user/{id}/withdraw')
async def user_fiat_withdraw(id, value: dict):
    user = DB.trader.user.find_one({"_id": ObjectId(id)})
    user = user_entity(user)
    new_balance = user["balance_brl"] - value["withdraw_value"]

    if new_balance < 0:
        return {"error_message": "There are not enough resources for the value of the withdrawal."}

    user["balance_brl"] = new_balance
    DB.trader.user.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(user)
    })
    serialized = user_entity(DB.trader.user.find_one({"_id": ObjectId(id)}))
    return serialized

from fastapi import APIRouter
from bson import ObjectId

from src.models.user import User
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
    return list_users()


@user.put('/user/{id}')
async def update_user(user: User):
    DB.trader.user.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(user)
    })
    serialized = users_entity(DB.trader.user.find_one({"_id": ObjectId(id)}))
    return serialized

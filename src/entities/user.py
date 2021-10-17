from bson import ObjectId

from src.database.db import DB
from src.schemas.user import user_entity


class UserMongo:

    def __init__(self, id):
        self.id = id

    def get(self):
        return user_entity(DB.trader.user.find_one({"_id": ObjectId(self.id)}))

    def update(self, user: dict):
        DB.trader.user.find_one_and_update({"_id": ObjectId(self.id)}, {
            "$set": user
        })

import os

from pymongo import MongoClient


CONN = MongoClient(os.environ["MONGODB_URL"])

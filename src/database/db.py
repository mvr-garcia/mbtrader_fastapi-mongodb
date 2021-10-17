import os

from pymongo import MongoClient


conn_str = os.environ["MONGODB_URL"]

# set a 5-second connection timeout
DB = MongoClient(conn_str, serverSelectionTimeoutMS=5000)

try:
    print(DB.server_info())
except Exception:
    print("Unable to connect to the server.")

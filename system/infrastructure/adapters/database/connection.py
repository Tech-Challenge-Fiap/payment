import os
from pymongo import MongoClient

db_port = os.environ.get("MONGO_PORT", 27017)
db_user = os.environ.get("MONGO_USERNAME", "myappuser")
db_pass = os.environ.get("MONGO_PASSWORD", "myapppassword")
db_host = os.environ.get("MONGO_HOST", "localhost")

config={
    "host": db_host,
    "port": db_port,
    "username":db_user,
    "password": db_pass
}

class Connection:
    def __new__(cls, database):
        connection=MongoClient(**config)
        return connection[database]
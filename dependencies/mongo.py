import key
from pymongo import MongoClient

client = MongoClient(key.MONGO_URL)
db = client.get_database('test')
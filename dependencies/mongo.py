import key
from pymongo.mongo_client import MongoClient
import certifi

client = MongoClient(key.MONGO_URL, tlsCAFile=certifi.where())
db = client.get_database('test')
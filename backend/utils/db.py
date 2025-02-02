from pymongo import MongoClient
import gridfs
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client.hackathon_db
fs = gridfs.GridFS(db)

users_collection = db.users

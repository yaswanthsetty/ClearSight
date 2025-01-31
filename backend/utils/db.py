from pymongo import MongoClient
import gridfs
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client.ai_risk_db
fs = gridfs.GridFS(db)

users_collection = db.users

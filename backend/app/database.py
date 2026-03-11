from pymongo import MongoClient

from app.config import COLLECTION_NAME, DB_NAME, MONGODB_URI


client = MongoClient(MONGODB_URI) if MONGODB_URI else None
db = client[DB_NAME] if client and DB_NAME else None
enterprise_collection = db[COLLECTION_NAME] if db and COLLECTION_NAME else None

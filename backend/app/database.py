from pymongo import MongoClient

from app.config import COLLECTION_NAME, DB_NAME, MONGODB_URI

client = MongoClient(MONGODB_URI) if MONGODB_URI else None
db = client[DB_NAME] if client is not None and DB_NAME else None
enterprise_collection = db[COLLECTION_NAME] if db is not None and COLLECTION_NAME else None
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import MONGO_URI, DB_NAME

class DBManager:
    def __init__(self):
        self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        self.db = self.client[DB_NAME]

    def get_collection(self, name):
        return self.db[name]

    def is_alive(self):
        try:
            self.client.admin.command('ping')
            return True
        except ConnectionFailure:
            return False

    @staticmethod
    def serialize_doc(doc):
        if not doc: return None
        doc['id'] = str(doc['_id'])
        del doc['_id']
        return doc

db_instance = DBManager()
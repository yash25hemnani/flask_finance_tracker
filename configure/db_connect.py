import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def connectToDB():
    client = MongoClient(os.environ.get('MONGODB_URI'))
    db = client['transaction_app']
    return db

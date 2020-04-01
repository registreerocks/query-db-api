from pymongo import MongoClient

CLIENT = MongoClient('mongodb://mongodb:27017/')
DB = CLIENT.database
query_details = DB.query_db

from os import environ as env

from pymongo import MongoClient

CLIENT = MongoClient(
  'mongodb://mongodb:27017/', 
  username=env.get('MONGO_USERNAME'), 
  password=env.get('MONGO_PASSWORD')
  )
DB = CLIENT.database
query_details = DB.query_db
student_details =  DB.student_db
joining_db = DB.joining_db

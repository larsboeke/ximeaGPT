from pymongo import MongoClient
from email_chunker import chunk_email
from get_cases_from_db import get_all_cases



# Create a MongoDB client
client = MongoClient('mongodb://192.168.11.30:27017/')

# Connect to your database
db = client['XIMEAGPT']

# Now you can use db to interact with your database

collection = db['prototype']

collection.delete_many({})

"""i = 0
anzahl_cases = len(get_all_cases())

for case in get_all_cases():
    i += 1
    print(i , "/" , anzahl_cases)
    db_instance = chunk_email(case)
    collection.insert_many(db_instance)"""

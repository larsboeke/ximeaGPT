from get_message import get_full_message_from_one_case
from get_cases_from_db import get_all_cases, get_new_cases
from email_chunker import chunk_email

# SOME EXAMPLES:

# Get all email cases
get_all_cases()

# Get all email cases, newer than x days
cases = get_new_cases(13)
print(cases)

# Get full message of example case "443028c8-a026-eb11-96e8-00155d0b2a0b"
case = get_full_message_from_one_case("443028c8-a026-eb11-96e8-00155d0b2a0b")

result = chunk_email("443028c8-a026-eb11-96e8-00155d0b2a0b")
print(result)
# Some example queries

case, metadata = get_full_message_from_one_case("44e1f779-96f4-ed11-9718-00155d0b2a0b")
case, metadata = get_full_message_from_one_case("f5fe8c80-88e2-ed11-9717-00155d0b2a0b")
print(case)
print(metadata)


# EXAMPLE of push into mongodb

from pymongo import MongoClient
from email_chunker import chunk_email
from get_cases_from_db import get_all_cases



# Create a MongoDB client
client = MongoClient('mongodb://192.168.11.30:27017/')

# Connect to your database
db = client['XIMEAGPT']

# Now you can use db to interact with your database

collection = db['prototype']

#collection.delete_many({})

i = 0
anzahl_cases = len(get_all_cases())

for case in get_all_cases():
    i += 1
    print(i , "/" , anzahl_cases)
    db_instance = chunk_email(case)
    collection.insert_many(db_instance)

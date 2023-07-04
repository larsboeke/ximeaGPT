import pymongo
from datetime import datetime as dt

client = pymongo.MongoClient('mongodb://192.168.11.30:27017/')
db = client['admin']                            
activity_mongo = db["feedback"]
# entry = {
#     chunk_id = xxx,
#     down_rating = 2
# }

def check_chunk_id(chunk_id):
    query = {"chunk_id": chunk_id}
    result = activity_mongo.find_one(query)
    return result is not None


def check_feedback(chunk_id):
    if check_chunk_id(chunk_id):
        activity_mongo.update_one({"chunk_id": chunk_id}, {"$inc": {"down_rating": 1}})
    else:
        new_entry = {"chunk_id": chunk_id, "down_rating": 1}
        activity_mongo.insert_one(new_entry)

def add_feedback(chunk_id):
    pass
    

def get_feedback():
    pass

def delete_chunk():
    pass
 
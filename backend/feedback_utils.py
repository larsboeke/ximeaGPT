import pymongo
from datetime import datetime as dt
from bson.objectid import ObjectId

client = pymongo.MongoClient('mongodb://192.168.11.30:27017/')
db = client['admin']                            
feedback_mongo = db["feedback"]
db2 = client['XIMEAGPT']
chunk_mongo = db2['prototype3']


# entry = {
#     chunk_id = xxx,
#     down_rating = 2
# }

def check_chunk_id(chunk_id):
    query = {"chunk_id": chunk_id}
    result = feedback_mongo.find_one(query)
    return result is not None


def add_feedback(chunk_id):
    if check_chunk_id(chunk_id):
        feedback_mongo.update_one({"chunk_id": chunk_id}, {"$inc": {"down_rating": 1}})
    else:
        new_entry = {"chunk_id": chunk_id, "down_rating": 1}
        feedback_mongo.insert_one(new_entry)

def get_all_chunk_ids():
    results = feedback_mongo.find({}, {"_id": 0, "chunk_id": 1})  # Get only the chunk_id field from all documents
    chunk_ids = [result["chunk_id"] for result in results]  # Extract chunk_id from each document
    return chunk_ids

def get_rating(chunk_id):
    query = {"chunk_id": chunk_id}
    result = feedback_mongo.find_one(query)
    return result

def get_content_metadata(chunk_id):
    query = {"_id": ObjectId(chunk_id)}
    results = chunk_mongo.find(query)
    entries = [result for result in results]
    return entries

def get_rated_chunk(chunk_id):
    rated_chunk = []
    rated_chunk.append(get_rating(chunk_id))
    rated_chunk.append(get_content_metadata(chunk_id))
    return(rated_chunk)


def reset_down_rating(chunk_id):
    feedback_mongo.update_one({"chunk_id": chunk_id}, {"$set": {"down_rating": 0}})


def delete_chunk():
    pass
 

chunk_id = "64a3e1fb385ee30652778033"

#add_feedback(chunk_id)
#print(get_rated_chunk(chunk_id))
print(get_all_chunk_ids())
reset_down_rating(chunk_id)
print(get_rating(chunk_id))


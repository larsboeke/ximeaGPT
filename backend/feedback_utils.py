import pymongo
from datetime import datetime as dt
from bson.objectid import ObjectId
from ..data_package.Pinecone_Connection_Provider import PineconeConnectionProvider
from ..data_package.MongoDB_Connection_Provider import MongoDBConnectionProvider


chunk_mongo = MongoDBConnectionProvider.MongoDBConnectionProvider().initMongoDB()
feedback_mongo = MongoDBConnectionProvider.MongoDBConnectionProvider().initFeedbackMongoDB()
index = PineconeConnectionProvider.PineconeConnectionProvider().initPinecone()



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
    feedback_mongo.delete_one({"chunk_id": chunk_id})  #Optionel -> Nicht Deleten sonder auf 0 setzen!


def get_all_rated_chunks():
    all_ratings = []
    for chunk_id in get_all_chunk_ids():
        all_ratings.append(get_rated_chunk(chunk_id))
    return all_ratings

def reset_all_down_ratings():
    for chunk_id in get_all_chunk_ids():
        reset_down_rating(chunk_id)


def delete_chunk(chunk_id):
    # Delete from MongoDB
    chunk_mongo.delete_one({"_id": ObjectId(chunk_id)})
    feedback_mongo.delete_one({"chunk_id": chunk_id})
    # Delete from Pinecone
    index.delete(ids=[chunk_id], namespace="pastConversations")

def clean_chunk(data):
    # Ensure the input is a list and has exactly two elements
    if isinstance(data, list) and len(data) == 2:
        dict1 = data[0]
        dict2 = data[1][0] if isinstance(data[1], list) and len(data[1]) > 0 else {}

        # Ensure both elements are dictionaries
        if isinstance(dict1, dict) and isinstance(dict2, dict):
            result = dict1.copy()  # Start with the first dictionary's keys and values
            result.update(dict2)  # Adds the second dictionary's keys and values
            return result

    # If the data does not match the expected structure, return an empty dictionary
    return {}

"""chunk_id = "64a3e1fb385ee30652778034"


add_feedback(chunk_id)"""
#print(get_rated_chunk(chunk_id))

"""all_feedback = get_all_rated_chunks()
print(all_feedback)
#print(all_feedback)
print("Merged:")"""

def get_all_cleaned_rated_chunks():
    cleaned_chunks = []
    for chunk in get_all_rated_chunks():
        cleaned_chunks.append(clean_chunk(chunk))
    return cleaned_chunks

#print(get_all_cleaned_rated_chunks())

index.delete(ids=["64a4003e8334c0a8ff7793d4"], namespace="pastConversations")
print("deleted")
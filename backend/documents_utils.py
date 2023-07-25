from dotenv import load_dotenv
import os
import openai
import pymongo
#import data_package.MongoDB_Connection_Provider.MongoDBConnectionProvider as MongoDBConnectionProvider
from bson import ObjectId,  json_util
import json

client = pymongo.MongoClient('mongodb://192.168.11.30:27017/')
db = client["XIMEAGPT"]
col = db["prototype"]

#col = MongoDBConnectionProvider.MongoDBConnectionProvider().initMongoDB()

def search_mongoDB(objectID=None, type=None, source=None, content=None, limit=None):

    query = {}
  
    if objectID:
        result = col.find_one(ObjectId(objectID))
        result['_id'] = str(result['_id'])
        return result

 
    if content:
        query["content"] = {"$regex": content}

    if type:
        query["metadata.type"] = type

    if source:
        query["metadata.source_id"] = {"$regex": source}

    if limit:
        result = col.find(query).limit(limit)
    else:
        result = col.find(query)

    list = []
    dict = {}
    for i in result:
        dict["_id"] = str(i['_id'])
        dict["content"] = i['content']
        dict["metadata"] = i['metadata']
        list.append(dict)
        
    return list

#id = "64baa27365c0bca14a31afa6"


# source_id = "https://www.ximea.com/support/projects/allprod/wiki/FAQ_-_Cooled_CCD_cameras"

# print(f"_______________SEARCH_____BY___________ID___________",search_mongoDB(objectID=id))
# docs = search_mongoDB(type="manuals", limit=2)
# for doc in docs:
#     print(doc)
# print(f"_______________SEARCH_____BY___________TYPE_________", search_mongoDB(type="manuals", limit=2, content=None))
#print(f"_______________SEARCH_____BY___________SOURCE_________", search_mongoDB(source=source_id, limit=2))
#print(f"_______________SEARCH_____BY___________Content_________",search_mongoDB(content="Sony Pregius", limit=2))
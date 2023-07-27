from dotenv import load_dotenv
import os
import openai
import pymongo
import data_package.MongoDB_Connection_Provider.MongoDBConnectionProvider as MongoDBConnectionProvider
from bson import ObjectId,  json_util
import json

col = MongoDBConnectionProvider.MongoDBConnectionProvider().initMongoDB()

# client = pymongo.MongoClient('mongodb://192.168.11.30:27017/')
# db = client["XIMEAGPT"]
# col = db["prototype"]

#col = MongoDBConnectionProvider.MongoDBConnectionProvider().initMongoDB()

def search_mongoDB(objectID=None, type=None, source=None, content=None, limit=None):

    query = {}

    try:
        if objectID:
            result = col.find_one(ObjectId(objectID))
            result['_id'] = str(result['_id'])
            liste = [result]
            return liste
    except:
        return []

 
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
    for i in result:
        list.append(i)
    
    for i in list:
        i['_id'] = str(i['_id'])

    return list

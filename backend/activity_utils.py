import pymongo
from datetime import datetime as dt

client = pymongo.MongoClient('mongodb://192.168.11.30:27017/')
db = client['admin']                            
activity_mongo = db["activity"]

def add_activity(embeddings_token, prompt_token, completion_token):
    timestamp = dt.now()

    embeddings_price = 0.0001
    prompt_price = 0.003
    completion_price = 0.004
    cost = embeddings_token * (embeddings_price/1000) + prompt_token * (prompt_price/1000) + completion_token * (completion_price/1000)

    entry = {
         'timestamp' : timestamp,
         'embeddings_token' : embeddings_token,
         'prompt_token' : prompt_token,
         'completion_token' : completion_token,
         'cost' : cost
    }



    activity_mongo.insert_one(entry)

def get_activity_count(startdate, enddate):
    pass

def get_activity_cost(startdate, enddate):
    pass
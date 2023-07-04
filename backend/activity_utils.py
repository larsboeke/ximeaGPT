import pymongo
from datetime import datetime as dt

client = pymongo.MongoClient('mongodb://192.168.11.30:27017/')
db = client['admin']                            
activity_mongo = db["activity"]

def add_activity(embeddings_token, prompt_token, completion_token, start_timestamp, end_timestamp):

    embeddings_price = 0.0001
    prompt_price = 0.003
    completion_price = 0.004
    cost = embeddings_token * (embeddings_price/1000) + prompt_token * (prompt_price/1000) + completion_token * (completion_price/1000)

    entry = {
         'start_timestamp' : start_timestamp,
         'end_timestamp' : end_timestamp,
         'embeddings_token' : embeddings_token,
         'prompt_token' : prompt_token,
         'completion_token' : completion_token,
         'cost' : cost
    }



    activity_mongo.insert_one(entry)

def get_avg_time_response(startdate, enddate):
    pipeline = [
        {
            '$match': {
                'start_timestamp': {'$gte': startdate, '$lte': enddate}
            }
        },
        {
            '$group': {
                '_id': None,
                'total_time': {'$sum': {'$subtract': ['$end_timestamp', '$start_timestamp']}},
                'count': {'$sum': 1}
            }
        },
        {
            '$project': {
                '_id': 0,
                'average_time': {'$divide': ['$total_time', '$count']}
            }
        }
    ]

    result = list(activity_mongo.aggregate(pipeline))
    if result:
        average_time = result[0]['average_time']
        return average_time
    else:
        return None

def get_activity_count(startdate, enddate):
    count = activity_mongo.count_documents(
        {"timestamp": {"$gte": startdate, "$lte": enddate}}
    )
    return count

def get_activity_cost(startdate, enddate):
    result = activity_mongo.find(
        [
            {
                "$match": {
                    "timestamp": {"$gte": startdate, "$lte": enddate}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_cost": {"$sum": "$cost"}
                }
            }
        ]
    )
    total_cost = list(result)[0]["total_cost"]
    return total_cost


def get_graph_activity(startdate, enddate):
    result = activity_mongo.aggregate(
        [
            {
                "$match": {
                    "timestamp": {"$gte": startdate, "$lte": enddate}
                }
            },
            {
                "$group": {
                    "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}},
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"_id": 1}
            }
        ]
    )
    graph_data = [{"date": entry["_id"], "count": entry["count"]} for entry in result]
    return graph_data



def generate_report(start_timestamp, end_timestamp):
    avg_response_time = get_avg_time_response(start_timestamp, end_timestamp)
    activity_count = get_activity_count(start_timestamp, end_timestamp)
    activity_cost = get_activity_cost(start_timestamp, end_timestamp)
    graph_data = get_graph_activity(start_timestamp, end_timestamp)

    report = {
        'avg_response_time' : avg_response_time,
        'activity_count' : activity_count,
        'activity_cost' : activity_cost,
        'graph_data' : graph_data
    }
    return report
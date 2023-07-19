import pymongo
import datetime as dt
from datetime import datetime

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
                'total_time': {'$sum': {'$divide': [{'$subtract': ['$end_timestamp', '$start_timestamp']}, 1000]}},
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
        avg_time_rounded = round(average_time, 2)
        
        return avg_time_rounded
    else:
        return None


def get_activity_count(startdate, enddate):
    count = activity_mongo.count_documents(
        {"start_timestamp": {"$gte": startdate, "$lte": enddate}}
    )
    return count

def get_activity_cost(startdate, enddate):
    pipeline = [
        {
            "$match": {
                "start_timestamp": {"$gte": startdate, "$lte": enddate}
            }
        },
        {
            "$group": {
                "_id": None,
                "total_cost": {"$sum": "$cost"}
            }
        }
    ]

    result = list(activity_mongo.aggregate(pipeline))
    print(result)
    if result:
        total_cost = result[0]['total_cost']
        rounded_total_cost = round(total_cost, 2)
        return rounded_total_cost
    else:
        return None

def get_cost_per_message(activity_cost, activity_count):
    if activity_cost is not None and activity_count != 0:
        cost_per_message = round(activity_cost/activity_count, 3)
        return cost_per_message
    else:
        return None

def get_graph_activity(startdate, enddate):
    #agregation by time when the selected daterange is 24 hours
    if startdate.date() == enddate.date(): 
        pipeline = [
            {
                "$match": {
                    "start_timestamp": {"$gte": startdate, "$lte": enddate}
                }
            },
            {
                "$group": {
                    "_id": {
                        "year": {"$year": "$start_timestamp"},
                        "month": {"$month": "$start_timestamp"},
                        "day": {"$dayOfMonth": "$start_timestamp"},
                        "hour": {"$hour": "$start_timestamp"}
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"_id": 1}
            }
        ]
    #agregation by days when the selected daterange is more than one day
    else:
        pipeline = [
            {
                "$match": {
                    "start_timestamp": {"$gte": startdate, "$lte": enddate}
                }
            },
            {
                "$group": {
                    "_id": {
                        "year": {"$year": "$start_timestamp"},
                        "month": {"$month": "$start_timestamp"},
                        "day": {"$dayOfMonth": "$start_timestamp"}
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"_id": 1}
            }
        ]

    result = activity_mongo.aggregate(pipeline)

    timestamp = []
    count = []

    for entry in result:
         timestamp_dict = entry["_id"]
         timestamp_obj = datetime(
            timestamp_dict["year"],
            timestamp_dict["month"],
            timestamp_dict["day"],
            timestamp_dict.get("hour", 0)
        )
         #convertion to ISO date format 
         timestamp.append(timestamp_obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
         count.append(entry["count"])

    #graph_data = [{"timestamp": timestamp, "count": count} for entry in result]
    graph_data = {"timestamp": timestamp, "count": count}

    return graph_data
    # result = activity_mongo.aggregate(
    #     [
    #         {
    #             "$match": {
    #                 "timestamp": {"$gte": startdate, "$lte": enddate}
    #             }
    #         },
    #         {
    #             "$group": {
    #                 "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}},
    #                 "count": {"$sum": 1}
    #             }
    #         },
    #         {
    #             "$sort": {"_id": 1}ed
    #         }
    #     ]
    # )
    # graph_data = [{"date": entry["_id"], "count": entry["count"]} for entry in result]
    #return graph_data



def generate_report(start_timestamp, end_timestamp):
    avg_response_time = get_avg_time_response(start_timestamp, end_timestamp)
    activity_count = get_activity_count(start_timestamp, end_timestamp)
    activity_cost = get_activity_cost(start_timestamp, end_timestamp)
    cost_per_message = get_cost_per_message(activity_cost, activity_count)
    graph_data = get_graph_activity(start_timestamp, end_timestamp)


    report = {
        'avg_response_time' : avg_response_time,
        'activity_count' : activity_count,
        'activity_cost' : activity_cost,
        'cost_per_message' : cost_per_message,
        'graph_data' : graph_data
    }
    return report

# start_date = dt.datetime(2023, 7, 1)
# end_date = dt.datetime.now()
# print(type(start_date))
# print(type(end_date))
# report = generate_report(start_date, end_date)
# print(report)
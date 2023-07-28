from upload.DatabaseCleaner import DatabaseCleaner
from data_package.Pinecone_Connection_Provider.PineconeConnectionProvider import PineconeConnectionProvider
from data_package.MongoDB_Connection_Provider.MongoDBConnectionProvider import MongoDBConnectionProvider
import time
from bson.objectid import ObjectId

mongodb_connection = MongoDBConnectionProvider().initMongoDB()
pinecone_connection = PineconeConnectionProvider().initPinecone()


"""pipeline = [
            {
                "$match": {
                    "metadata.type": "email"
                }
            },
            {
                "$group": {
                    "_id": "$content",
                    # _id should be the first ten characters of the content
                    # "_id": { "$substr": ["$content", 0, 10] },
                    "count": {"$sum": 1},
                    "documents": {"$push": "$$ROOT"}
                }
            },
            {
                "$match": {
                    "count": {"$gt": 1}
                }
            }
        ]

result = list(mongodb_connection.aggregate(pipeline))
print("Deleting number of chunks that are in the DB more than once: ", len(result))
"""
source = {'id': '64baa27365c0bca14a31afae', 'content': 'Please clarify the country and company of your inquiry:\nDear ximea Team,\xa0\n\n\nwe, Conphis are distributors of proccesing equipment for SE Europe (ex-yugoslav cointries). One of my customers is looking for multispectral agriculture dron surveillance and your model\xa0MQ022HG-IM-SM5X5-NIR2\xa0\n\nseem to fit perfectly except of resolution which is required to be higher.\xa0\nAlso they would like to connect it to Raspberry Pi. Is this possible?\n\n\nAnyway they would like to know price for this model (1 pc).', 'metadata': {'type': 'email', 'source_id': '8ca19a61-3941-eb11-96e8-00155d0b2a0b', 'activity_id': ['3b058f5b-3941-eb11-96e8-00155d0b2a0b', '107704c3-7e43-eb11-96e8-00155d0b2a0b', '8aee3b00-a043-eb11-96e8-00155d0b2a0b'], 'document_date': ['2020-12-18 14:00:22', '2020-12-21 11:22:18', '2020-12-21 15:20:05'], 'order_id': 0}}
source_id = source["metadata"]["source_id"]
order_id = source["metadata"]["order_id"]
print("order: ", order_id+1)
query = {
    "metadata.source_id": source_id,
    "metadata.order_id": {"$eq": order_id+5}
}
source_extra = mongodb_connection.find(query)
result = list(source_extra)

if result:
    result = result[0]
    result["id"] = result.pop("_id")
    result["id"] = str(result["id"])
    print("Source extra: ", result)
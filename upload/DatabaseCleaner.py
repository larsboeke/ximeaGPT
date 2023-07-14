from bson.objectid import ObjectId

class DatabaseCleaner:
    def __init__(self, mongodb_connection, pinecone_connection):
        self.mongodb_connection = mongodb_connection
        self.pinecone_connection = pinecone_connection
    def delete_chunk(self, chunk_id):
        # Delete from MongoDB
        self.mongodb_connection.delete_one({"_id": ObjectId(chunk_id)})
        # Delete from Pinecone
        print(f"deleted chunk {chunk_id} from pinecone")
        self.pinecone_connection.delete(ids=[chunk_id], namespace="pastConversations")

    def delete_short_chunks(self):
        query = {
            "$expr": { "$lt": [{ "$strLenCP": "$content" }, 100] },
            "metadata.type": "email"
        }
        result = self.mongodb_connection.find(query)
        chunks = [document for document in result]
        print("Deleting chunks with less than 100 characters: ", len(chunks))

        for chunk in chunks:
            self.delete_chunk(str(chunk['_id']))


    def remove_duplicates_from_databases(self):
        pipeline = [
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
        # Execute the aggregation pipeline
        result = list(self.mongodb_connection.aggregate(pipeline))
        print("Deleting number of chunks that are in the DB more than once: ", len(result))
        if len(result) != 0:
            for document in result:
                for duplicate in document['documents']:
                    if duplicate['_id'] != document['documents'][0]['_id']:
                        self.delete_chunk(str(duplicate['_id']))

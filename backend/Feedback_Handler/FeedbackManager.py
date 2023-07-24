import pymongo
from datetime import datetime as dt
from bson.objectid import ObjectId
import data_package.Pinecone_Connection_Provider.PineconeConnectionProvider as PineconeConnectionProvider
import data_package.MongoDB_Connection_Provider.MongoDBConnectionProvider as MongoDBConnectionProvider
import backend.Feedback_Handler.FeedbackProvider as FeedbackProvider


class FeedbackManager:
    def __init__(self):
        """
        :param pinecone_connection:
        :param mongodb_chunk:
        :param sql_connection:
        """
        self.pinecone_connection = PineconeConnectionProvider.PineconeConnectionProvider().initPinecone()
        self.chunk_mongo = MongoDBConnectionProvider.MongoDBConnectionProvider().initMongoDB()
        self.feedback_mongo = MongoDBConnectionProvider.MongoDBConnectionProvider().initFeedbackMongoDB()


    def check_chunk_id(self, chunk_id):
        query = {"chunk_id": chunk_id}
        result = self.feedback_mongo.find_one(query)
        return result is not None


    def add_feedback(self, chunk_id):
        if self.check_chunk_id(chunk_id):
            self.feedback_mongo.update_one({"chunk_id": chunk_id}, {"$inc": {"down_rating": 1}})
        else:
            new_entry = {"chunk_id": chunk_id, "down_rating": 1}
            self.feedback_mongo.insert_one(new_entry)

    def reset_down_rating(self, chunk_id):
        self.feedback_mongo.delete_one({"chunk_id": chunk_id}) 


    def reset_all_down_ratings(self):
        for chunk_id in FeedbackProvider().get_all_chunk_ids():
            self.reset_down_rating(chunk_id)


    def delete_chunk(self, chunk_id):
        # Delete from MongoDB
        self.chunk_mongo.delete_one({"_id": ObjectId(chunk_id)})
        self.feedback_mongo.delete_one({"chunk_id": chunk_id})
        # Delete from Pinecone (test every namespace)
        self.pinecone_connection.delete(ids=[chunk_id], namespace="tickets")
        self.pinecone_connection.delete(ids=[chunk_id], namespace="emails")
        self.pinecone_connection.delete(ids=[chunk_id], namespace="manuals")


    
    
import pymongo
from datetime import datetime as dt
from bson.objectid import ObjectId
import data_package.Pinecone_Connection_Provider.PineconeConnectionProvider as PineconeConnectionProvider
import data_package.MongoDB_Connection_Provider.MongoDBConnectionProvider as MongoDBConnectionProvider


class Feedback_Handler:
    def __init__(self):
        """
        :param pinecone_connection:
        :param mongodb_chunk:
        :param sql_connection:
        """
        self.pinecone_connection = PineconeConnectionProvider.PineconeConnectionProvider().initPinecone()
        self.chunk_mongo = MongoDBConnectionProvider.MongoDBConnectionProvider().initMongoDB()
        self.feedback_mongo = MongoDBConnectionProvider.MongoDBConnectionProvider().initFeedbackMongoDB()

# entry = {
#     chunk_id = xxx,
#     down_rating = 2
# }

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

    def get_all_chunk_ids(self):
        results = self.feedback_mongo.find({}, {"_id": 0, "chunk_id": 1})  # Get only the chunk_id field from all documents
        chunk_ids = [result["chunk_id"] for result in results]  # Extract chunk_id from each document
        return chunk_ids

    def get_rating(self, chunk_id):
        query = {"chunk_id": chunk_id}
        result = self.feedback_mongo.find_one(query)
        return result

    def get_content_metadata(self, chunk_id):
        query = {"_id": ObjectId(chunk_id)}
        results = self.chunk_mongo.find(query)
        entries = [result for result in results]
        return entries

    def get_rated_chunk(self, chunk_id):
        rated_chunk = []
        rated_chunk.append(self.get_rating(chunk_id))
        rated_chunk.append(self.get_content_metadata(chunk_id))
        return(rated_chunk)


    def reset_down_rating(self, chunk_id):
        self.feedback_mongo.delete_one({"chunk_id": chunk_id})  #Optionel -> Nicht Deleten sonder auf 0 setzen!


    def get_all_rated_chunks(self):
        all_ratings = []
        for chunk_id in self.get_all_chunk_ids():
            all_ratings.append(self.get_rated_chunk(chunk_id))
        return all_ratings

    def reset_all_down_ratings(self):
        for chunk_id in self.get_all_chunk_ids():
            self.reset_down_rating(chunk_id)


    def delete_chunk(self, chunk_id):
        # Delete from MongoDB
        self.chunk_mongo.delete_one({"_id": ObjectId(chunk_id)})
        self.feedback_mongo.delete_one({"chunk_id": chunk_id})
        # Delete from Pinecone (test every namespace)
        self.pinecone_connection.delete(ids=[chunk_id], namespace="tickets")
        self.pinecone_connection.delete(ids=[chunk_id], namespace="emails")
        self.pinecone_connection.delete(ids=[chunk_id], namespace="manuals")

    def clean_chunk(self, data):
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


    def get_all_cleaned_rated_chunks(self):
        cleaned_chunks = []
        for chunk in self.get_all_rated_chunks():
            cleaned_chunks.append(self.clean_chunk(chunk))
        return cleaned_chunks


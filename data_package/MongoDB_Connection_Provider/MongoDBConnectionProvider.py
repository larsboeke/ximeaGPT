import pymongo
from pymongo import MongoClient, UuidRepresentation

class MongoDBConnectionProvider:
    def initMongoDB(self):
        """
        Initialise a connection to our MongoDB database
        :return mongodb_connection: collection name of the database to connect to
        """
        # Initialise the non structured database MongoDB
        client = pymongo.MongoClient("mongodb://192.168.11.30:27017/", uuidRepresentation= UuidRepresentation.STANDARD)
        db = client["XIMEAGPT"]
        mongodb_connection = db["prototype2"]
        return mongodb_connection
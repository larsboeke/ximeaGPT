import pymongo


class MongoDBConnectionProvider:
    def initMongoDB(self):
        """
        Initialise a connection to our MongoDB database
        :return mongodb_connection: collection name of the database to connect to
        """
        # Initialise the non structured database MongoDB
        client = pymongo.MongoClient("DELETED")
        db = client["XIMEAGPT"]
        mongodb_connection = db["prototype"]
        return mongodb_connection

    def initFeedbackMongoDB(self):
        """
        Initialise a connection to our MongoDB database
        :return mongodb_connection: collection name of the database to connect to
        """
        # Initialise the non structured database MongoDB
        client = pymongo.MongoClient("DELETED")
        db = client["XIMEAGPT"]
        mongodb_connection = db["feedback"]
        return mongodb_connection

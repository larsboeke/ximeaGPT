import pymongo

class MongoDBConnectionProvider:
    def initMongoDB(self):
        """
        Initialise a connection to our MongoDB database
        :return col: collection name of the database to connect to
        """
        # Initialise the non structured database MongoDB
        client = pymongo.MongoClient("mongodb://192.168.11.30:27017/")
        db = client["XIMEAGPT"]
        col = db["prototype"]
        return col
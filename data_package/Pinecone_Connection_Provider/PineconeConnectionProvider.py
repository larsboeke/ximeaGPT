import pinecone
import os
from dotenv import load_dotenv

load_dotenv()

class PineconeConnectionProvider:
    def __init__(self):
        self.PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
        self.PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT")
        self.PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME")

    def initPinecone(self):
        """
        Initialise a connection to our Pinecone database
        :return index: collection/index name of the database to connect to
        """
        pinecone.init(
            api_key=self.PINECONE_API_KEY,
            environment=self.PINECONE_ENVIRONMENT
        )
        index = pinecone.Index(self.PINECONE_INDEX_NAME)
        return index
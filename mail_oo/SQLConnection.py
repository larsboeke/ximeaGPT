from dotenv import load_dotenv
import os
import pymssql

load_dotenv()  # load environment variables from .env file

class SQLConnectionProvider:
    def __init__(self): 
        self.server = os.getenv('SQL_SERVER')
        self.database = os.getenv('SQL_DATABASE')
        self.username = os.getenv('SQL_USERNAME')
        self.password = os.getenv('SQL_PASSWORD')
        self.connection, self.cursor = self.create_connection()

    # create connection to SQL Server database
    def create_connection(self):
        connection = pymssql.connect(self.server, self.username, self.password, self.database)
        cursor = connection.cursor()
        return connection, cursor



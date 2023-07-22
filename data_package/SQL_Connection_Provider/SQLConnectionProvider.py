from dotenv import load_dotenv
import os
import pymssql
import mysql.connector

load_dotenv()  # load environment variables from .env file #sd

class SQLConnectionProvider:
    def __init__(self):
        self.server = os.getenv('SQL_SERVER')
        self.database = os.getenv('SQL_DATABASE')
        self.username = os.getenv('SQL_USERNAME')
        self.password = os.getenv('SQL_PASSWORD')
        
    # create connection to SQL Server database
    def create_connection(self):
        """
        Create a connection to the SQL Server database
        :return connection, cursor: connection and cursor objects
        """
        destination_host = '127.0.0.1'
        destination_database = 'prototype'
        destination_username = 'root'
        destination_password = '859760Si.'  
        connection = mysql.connector.connect(host=destination_host,
        database=destination_database,
        user=destination_username,
        password=destination_password,
        )
        cursor = connection.cursor()
        return connection, cursor



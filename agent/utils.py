import mysql.connector

def create_connection():
    connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="859760Si.",
    database="products3"
    )

    cursor = connection.cursor()
    return connection, cursor
create_connection()
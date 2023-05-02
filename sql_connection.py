import mysql.connector


#create connection to sql database
def create_connection():
    connection = mysql.connector.connect(
        host="your_host",
        user="your_username",
        password="your_password",
        database="your_database"
    )
    cursor = connection.cursor()
    return connection, cursor



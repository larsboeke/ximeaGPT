import mysql.connector


#create connection to sql database
def create_connection():
    connection = mysql.connector.connect(
        host="your_host",
        user="your_username",
        password="your_password",
        database="your_database"
    )
    return connection

def insert_data(id, content, date, communicationPartner, source):
    connection = create_connection()
    cursor = connection.cursor()
    sql_query = f"INSERT INTO your_table_name (id, content, date, communicationpartner, sourcee) VALUES ({id}, {content}, {date}, {communicationPartner}, {source})"
    cursor.execute(sql_query)
    connection.commit()
    print(f"{cursor.rowcount} record(s) inserted.")



def query_data(id):
    connection = create_connection()
    cursor = connection.cursor()
    sql_query = "SELECT * FROM your_table_name"
    cursor.execute(sql_query)
    results = cursor.fetchall()

    for row in results:
        print(row)

    return content, date, communicationpartner, source
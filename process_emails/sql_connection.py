import pymssql

# create connection to SQL Server database
def create_connection():
    server = '192.168.11.22'
    database = 'AI:Lean'
    username = 'AI:Lean'
    password = 'NbIxyuc5b!4'

    connection = pymssql.connect(server, username, password, database)
    cursor = connection.cursor()
    return connection, cursor

# retrieve top 100 entries from CrmEmails table
def get_top_100_emails():
    connection, cursor = create_connection()
    query = "SELECT TOP 100 * FROM [AI:Lean].[dbo].[CrmEmails]"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    return results


import pyodbc

# create connection to SQL Server database
def create_connection():
    server = 'SRV-XIM04'
    database = 'AI:Lean'
    username = 'AI:Lean'
    password = 'NbIxyuc5b!4'
    driver= '{ODBC Driver 17 for SQL Server}' # or '{SQL Server Native Client 11.0}' for older versions of SQL Server

    connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    connection = pyodbc.connect(connection_string)
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

# print top 100 entries from CrmEmails table
results = get_top_100_emails()
for row in results:
    print(row)
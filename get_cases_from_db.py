import sql_connection
from get_message import create_uncleaned_history, clean_uncleaned_history
def get_all_cases():
    connection, cursor = sql_connection.create_connection()
    query = "SELECT [regardingobjectid] from [AI:Lean].[dbo].[CrmEmails] ORDER BY [createdon] ASC"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    return results
# eg print all
# print(get_all_cases())

# important later after initial commit
def get_new_cases(days_back):
    connection, cursor = sql_connection.create_connection()
    query = "SELECT [regardingobjectid] from [AI:Lean].[dbo].[CrmEmails] " \
            "WHERE [createdon] > DATEADD(DAY, -%s, GETDATE()) ORDER BY [createdon] ASC"
    cursor.execute(query, (days_back,))
    results = cursor.fetchall()
    connection.close()
    return results
# eg 13 days minus today
# print(get_new_cases(13))

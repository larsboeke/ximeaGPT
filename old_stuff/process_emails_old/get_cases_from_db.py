from .sql_connection import create_connection

# Get all cases from Ximea, containing a unique list of UUIDs

def get_all_cases():
    connection, cursor = create_connection()
    query = "SELECT DISTINCT [regardingobjectid] from [AI:Lean].[dbo].[CrmEmails]"
    # not distinct but ordered by date: SELECT [regardingobjectid] from [AI:Lean].[dbo].[CrmEmails] ORDER BY [createdon] ASC
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    return results

# important later after initial commit / not useful atm
def get_new_cases(days_back):
    connection, cursor = create_connection()
    query = "SELECT DISTINCT [regardingobjectid] from [AI:Lean].[dbo].[CrmEmails] " \
            "WHERE [createdon] > DATEADD(DAY, -%s, GETDATE())"
    cursor.execute(query, (days_back,))
    results = cursor.fetchall()
    connection.close()
    return results


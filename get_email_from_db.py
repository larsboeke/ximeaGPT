import sql_connection

def get_entries_with_description(earliest_fetch_date):

    # connect to email sql database
    connection, cursor = sql_connection.create_connection()

    # Execute the SQL query

    # name der database muss noch geändert werden
    # just fetch after specific date:
    cursor.execute("SELECT Description, CreatedOn, Sender FROM email_database WHERE CreatedOn >= ?", earliest_fetch_date)

    # Fetch all rows
    emails = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Return the rows
    return emails

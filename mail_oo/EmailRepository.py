from SQLConnectionProvider import SQLConnectionProvider
from Email import Email

class EmailRepository:
    def __init__(self, sql_connection):
        self.connection, self.cursor = sql_connection

    def get_emails_for_case(self, caseid):
        emails = []  # Initialize an empty list for emails
        query = "SELECT [activityid], [description], [regardingobjectid], [createdon] FROM [AI:Lean].[dbo].[CrmEmails] " \
                "WHERE [regardingobjectid] = %s ORDER BY [createdon] ASC"
        self.cursor.execute(query, (caseid,))
        text_w_metadata = self.cursor.fetchall()
        #connection.close()

        # Convert each email in the list to an Email object and add to the list
        for email in text_w_metadata:
            email_obj = Email(*email)
            emails.append(email_obj)

        return emails

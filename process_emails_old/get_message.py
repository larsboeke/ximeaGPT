from . import sql_connection
from .clean_email import clean_message
from .clean_email import Email


class Case:
    def __init__(self, caseid):
        self.caseid = caseid
        self.emails = []
        self.set_case()

    def add_email(self, email: Email):
        self.emails.append(email)

    def remove_email(self, email: Email):
        self.emails.remove(email)

    def get_emails(self):
        return self.emails

    def set_case(self):
        self.emails = []  # Clear the existing emails
        connection, cursor = sql_connection.create_connection()
        query = "SELECT [activityid], [description], [regardingobjectid], [createdon] FROM [AI:Lean].[dbo].[CrmEmails] " \
                "WHERE [regardingobjectid] = %s ORDER BY [createdon] ASC"
        cursor.execute(query, (self.caseid,))
        text_w_metadata = cursor.fetchall()
        connection.close()

        # Convert each email in the list to an Email object
        for email in text_w_metadata:
            email_obj = Email(*email)
            self.add_email(email_obj)

# Extract email contents from tuple and create list out of it
def create_uncleaned_history(text_w_metadata):
    descriptions = [t[1] for t in text_w_metadata]

    email_list = []
    for description in descriptions:
        email_list.append(description)
    return email_list

# Clean each email content in list (eg remove html. signatures, greetings, etc...)
def clean_uncleaned_history(uncleaned_history):

    cleaned_history = []
    for message in uncleaned_history:
        cleaned_history.append(clean_message(message))
    return cleaned_history

def unify_email_list(cleaned_history):
    unified_emails = []

    for i in range(len(cleaned_history)):
        if i == 0:
            unified_emails.append(cleaned_history[0])
        elif i > 0:
            prev_email = unified_emails[i-1]
            prev_email_splitted = prev_email[:50]

            if prev_email_splitted != "":
                cleaned_email = cleaned_history[i].split(prev_email_splitted)[0]
                unified_emails.append(cleaned_email)
            else:
                unified_emails.append("No previous email exists. " + cleaned_history[i])
    return unified_emails

def get_full_message_from_one_case(caseid):
    text_w_metadata = get_activities_from_specific_case(caseid)
    uncleaned_history = create_uncleaned_history(text_w_metadata)
    cleaned_history = clean_uncleaned_history(uncleaned_history)
    unique_history = unify_email_list(cleaned_history)
    full_message = ''.join(unique_history)

    # get correct formatted dates for each Activity
    dates = [t[3] for t in text_w_metadata]
    formatted_dates = []
    for dt_obj in dates:
        formatted_dt = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
        formatted_dates.append(formatted_dt)

    metadata = {"type": "email",
                     "case_id": str(text_w_metadata[0][2]),
                     "activity_id": [str(t[0]) for t in text_w_metadata],
                     "document_date": formatted_dates
                     }

    return full_message, metadata




from Email import Email
from EmailRepository import EmailRepository
from PlainTextFromEmailProvider import PlainTextFromEmailProvider

class Case:
    def __init__(self, caseid, sql_connection):
        self.caseid = caseid
        self.emails = []
        self.metadata = {}
        self.set_case(caseid, sql_connection)

    def add_email(self, email: Email):
        self.emails.append(email)

    def remove_email(self, email: Email):
        self.emails.remove(email)

    def get_emails(self):
        return self.emails
    
    def set_case(self, caseid, sql_connection):
        email_for_one_case = EmailRepository().get_emails_for_case(caseid, sql_connection)
        activityids = []
        createdons = []
        
        for email in email_for_one_case:
            cleaned_email = PlainTextFromEmailProvider().clean_email(email)
            self.emails.append(cleaned_email)
            activityids.append(email.activityid)
            createdons.append(email.createdon)

        formatted_dates = []
        for dt_obj in createdons:
            formatted_dt = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
            formatted_dates.append(formatted_dt)
        
        self.metadata = {"type": "email",
                     "case_id": caseid,
                     "activity_id": activityids,
                     "document_date": formatted_dates
                     }
    
        
    
    



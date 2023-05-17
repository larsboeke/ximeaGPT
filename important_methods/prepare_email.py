import clean_text
import get_email_from_db

# earliest_fetch_date:  The emails will be fetched starting from a certain date
# index:                Identify which email needs to be fetched after the earliest_fetch_date
def prepare_email(earliest_fetch_date, index):

    # Get email from SQL DB
    email = get_email_from_db.get_entries_with_description(earliest_fetch_date=earliest_fetch_date)[index]
    print(email)
    print(type(email))
    """ Example of all_emails
    Description	    CreatedOn	            Sender
    "exampletxt1"	2022-04-30 10:30:00.00	aitest@ximea.de
    """

    # Clean the text and get the other relevant values
    # Output structure: text, date, communicationPartner, source
    email = clean_text(email)
    return email

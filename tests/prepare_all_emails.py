from important_methods import get_email_from_db, clean_text


def prepare_all_emails():
    # Get emails from SQL DB
    all_emails = get_email_from_db.get_entries_with_description("TEST Connection String")

    """ Example of all_emails
    Description	    CreatedOn	            Sender
    "exampletxt1"	2022-04-30 10:30:00.00	aitest@ximea.de
    "exampletxt2"	2022-04-29 09:45:00.00	kobie@brc.com
    """

    # Create a list to store the cleaned data
    cleaned_emails = []
    for email in all_emails:
        # Clean the text and get the other relevant values
        text, date, communicationPartner, source = clean_text(email)

        # Add the cleaned data to the list
        cleaned_emails.append((text, date, communicationPartner, source))

    return cleaned_emails

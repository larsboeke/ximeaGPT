import sql_connection
from clean_email import clean_message

#get_cases_from_db.get_new_cases()
#results = get_activities_from_specific_case("443028c8-a026-eb11-96e8-00155d0b2a0b")
#print(results[0][0])

# Input: specific caseid
# Output: a list of this format: [(activityid, description)(activityid, description)...]
def get_activities_from_specific_case(caseid):
    connection, cursor = sql_connection.create_connection()
    query = "SELECT [activityid], [description], [regardingobjectid], [createdon] FROM [AI:Lean].[dbo].[CrmEmails] " \
            "WHERE [regardingobjectid] = %s ORDER BY [createdon] ASC"
    cursor.execute(query, (caseid,))
    text_w_metadata = cursor.fetchall()
    connection.close()
    return text_w_metadata

#result  = get_activities_from_specific_case("443028c8-a026-eb11-96e8-00155d0b2a0b")
#activity, description = get_activities_from_specific_case("443028c8-a026-eb11-96e8-00155d0b2a0b")
#print(description)

def create_uncleaned_history(text_w_metadata):
    descriptions = [t[1] for t in text_w_metadata]

    email_list = []
    for description in descriptions:
        email_list.append(description)
    return email_list

#results = get_activities_from_specific_case("443028c8-a026-eb11-96e8-00155d0b2a0b")
#results = create_uncleaned_history(results)
#print(results)

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
                unified_emails.append("Previous not found. Error 187! " + cleaned_history[i])
    return unified_emails

"""def unify_email_list(cleaned_history):
    unified_emails = []

    for i in range(len(cleaned_history)):
        if cleaned_history[0] == cleaned_history[1] and i==0:
            unified_emails.append(cleaned_history[0])
        elif cleaned_history[0] == cleaned_history[1] and i==1:
            unified_emails.append("Previous not found. Error 187! ")
        elif i == 0:
            unified_emails.append(cleaned_history[0])

        elif i > 0:
            prev_email = unified_emails[i-1]
            prev_email_splitted = prev_email[:50]
            #print("History:" + cleaned_history[i])

            if prev_email_splitted != "":
                cleaned_email = cleaned_history[i].split(prev_email_splitted)[0]
                unified_emails.append(cleaned_email)
            else:
                unified_emails.append("Previous not found. Error 187! " + cleaned_history[i])
            #print("Prev Email:" + prev_email_splitted)
    return unified_emails"""

#uncleaned = create_uncleaned_history("443028c8-a026-eb11-96e8-00155d0b2a0b")
#print(uncleaned[0])
#cleaned = clean_uncleaned_history(uncleaned)

def get_full_message_from_one_case(caseid):
    act_desc_tuple = get_activities_from_specific_case(caseid)
    uncleaned_history = create_uncleaned_history(act_desc_tuple)
    cleaned_history = clean_uncleaned_history(uncleaned_history)
    unique_history = unify_email_list(cleaned_history)
    full_message = ''.join(unique_history)

    # get correct formatted dates for each Activity
    dates = [t[3] for t in act_desc_tuple]
    formatted_dates = []
    for dt_obj in dates:
        formatted_dt = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
        formatted_dates.append(formatted_dt)

    metadata = {"CaseID": str(act_desc_tuple[0][2]),
                     "ActivityID": [str(t[0]) for t in act_desc_tuple],
                     "DocumentDate": formatted_dates
                     }

    return full_message, metadata


#results = get_full_message_from_one_case("443028c8-a026-eb11-96e8-00155d0b2a0b")
#print(results)




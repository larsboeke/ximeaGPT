import sql_connection
from clean_email import get_newest_message

#get_cases_from_db.get_new_cases()
#results = get_activities_from_specific_case("443028c8-a026-eb11-96e8-00155d0b2a0b")
#print(results[0][0])

# Input: specific caseid
# Output: a list of this format: [(activityid, description)(activityid, description)...]
def get_activities_from_specific_case(caseid):
    connection, cursor = sql_connection.create_connection()
    query = "SELECT [activityid], [description] FROM [AI:Lean].[dbo].[CrmEmails] " \
            "WHERE [regardingobjectid] = %s ORDER BY [createdon] ASC"
    cursor.execute(query, (caseid,))
    results = cursor.fetchall()
    connection.close()
    return results

#result  = get_activities_from_specific_case("443028c8-a026-eb11-96e8-00155d0b2a0b")
#activity, description = get_activities_from_specific_case("443028c8-a026-eb11-96e8-00155d0b2a0b")
#print(description)

def create_uncleaned_history(act_desc_tuple):
    descriptions = [t[1] for t in act_desc_tuple]

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
        cleaned_history.append(get_newest_message(message))
    return cleaned_history

#uncleaned = create_uncleaned_history("443028c8-a026-eb11-96e8-00155d0b2a0b")
#print(uncleaned[0])
#cleaned = clean_uncleaned_history(uncleaned)

def get_full_message_from_one_case(caseid):
    act_desc_tuple = get_activities_from_specific_case(caseid)
    uncleaned_history = create_uncleaned_history(act_desc_tuple)
    cleaned_history = clean_uncleaned_history(uncleaned_history)

    full_message = ''.join(cleaned_history)

    return full_message


results = get_full_message_from_one_case("443028c8-a026-eb11-96e8-00155d0b2a0b")
print(results)




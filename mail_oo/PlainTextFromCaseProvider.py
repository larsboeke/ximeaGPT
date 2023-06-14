class PlainTextFromCaseProvider:
    
    def provide_full_content(case):
        unified_emails = []

        for i in range(len(case.emails)):
            if i == 0:
                unified_emails.append(case.emails[0])
            elif i > 0:
                prev_email = unified_emails[i-1]
                prev_email_splitted = prev_email[:50]

                if prev_email_splitted != "":
                    cleaned_email = case.emails[i].split(prev_email_splitted)[0]
                    unified_emails.append(cleaned_email)
                else:
                    unified_emails.append("No previous email exists. " + case.emails[i])
        full_content = ''.join(unified_emails)
        return full_content
    

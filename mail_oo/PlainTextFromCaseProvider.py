class PlainTextFromCaseProvider:

    def remove_identical_emails(self, emails):
        """
        Remove identical emails in given email list
        :param emails: list of emails
        :return emails: list of emails without duplicates
        :rtype: list
        """
        seen_emails = set()
        i = 0
        while i < len(emails):
            if emails[i] in seen_emails:
                emails.pop(i)
            else:
                seen_emails.add(emails[i])
                i += 1
        return emails

    def provide_full_content(self, case):
        """
        Provide the full content
        :param case:
        :return full_content: full content of the case
        :rtype: str
        """
        unified_emails = []

        case.emails = self.remove_duplicates(case.emails)

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
    

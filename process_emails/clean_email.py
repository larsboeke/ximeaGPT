"""from bs4 import BeautifulSoup


import re

def remove_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    return text

# method to remove last greeting
def remove_last_greeting(text):
    end_keywords = ["Best regards", "best regards", "Sincerely", "Kind regards", "Regards", "Best wishes",
                    "Yours faithfully", "Yours sincerely", "Warm regards", "All the best",
                    "Cheers", "Take care", "Have a nice day", "With appreciation", "Cordially",
                    "Viele Grüße", "Mit freundlichen Grüßen", "Herzliche Grüße", "Liebe Grüße",
                    "Alles Gute", "In freundschaftlicher Verbundenheit", "Hochachtungsvoll",
                    "Beste Wünsche", "Auf Wiedersehen", "Bis bald", "Pass auf dich auf",
                    "Schönen Tag noch", "Mit Dank und besten Grüßen", "Herzlichst", "Liebevoll",
                    "Mit freundlichem Gruß", "Gruß", "Beste Grüße", "LG", "MfG", "Thanks again and best regards"]
    for keyword in end_keywords:
        if keyword in text:
            text = text.split(keyword)[0]
    return text

def remove_greeting_to_subject(text):
    patterns = [r"From:.*?Subject:", r"Best regards.*?Subject:", r"Sincerely.*?Subject:",
                    r"Best regards.*?Subject:", r"Kind regards.*?Subject:", r"Regards.*?Subject:",
                    r"Best wishes.*?Subject:", r"Yours faithfully.*?Subject:", r"Yours sincerely.*?Subject:",
                    r"Warm regards.*?Subject:", r"All the best.*?Subject:", r"Cheers.*?Subject:",
                    r"Take care.*?Subject:", r"Have a nice day.*?Subject:", r"With appreciation.*?Subject:",
                    r"Cordially.*?Subject:", r"Viele Grüße.*?Subject:", r"Mit freundlichen Grüßen.*?Subject:",
                    r"Herzliche Grüße.*?Subject:", r"Liebe Grüße.*?Subject:", r"Alles Gute.*?Subject:",
                    r"In freundschaftlicher Verbundenheit.*?Subject:", r"Hochachtungsvoll.*?Subject:",
                    r"Beste Wünsche.*?Subject:", r"Auf Wiedersehen.*?Subject:", r"Bis bald.*?Subject:",
                    r"Pass auf dich auf.*?Subject:", r"Schönen Tag noch.*?Subject:", r"Mit Dank und besten Grüßen.*?Subject:",
                    r"Herzlichst.*?Subject:", r"Liebevoll.*?Subject:", r"Mit freundlichem Gruß.*?Subject:",
                    r"Gruß.*?Subject:", r"Beste Grüße.*?Subject:", r"LG.*?Subject:", r"MfG.*?Subject:",
                    r"Thanks again and best regards.*?Subject:"]
    for pattern in patterns:
        text = re.sub(pattern, "", text, flags=re.DOTALL)
        text = text.strip()
    return text


def remove_from_to_subject(text):
    pattern = r"From:.*?Subject:"
    text = re.sub(pattern, "", text, flags=re.DOTALL)
    text.strip()
    return text


# input is unclean html text with signature
# output is clened text without signatures and other unnecessary stuff
def clean_message(text):
    text = remove_html(text)
    text = remove_greeting_to_subject(text)
    text = remove_from_to_subject(text)
    text = remove_last_greeting(text)
    return text

"""

from bs4 import BeautifulSoup
import re

class Email:
    def __init__(self, activityid, description, regardingobjectid, createdon):
        self.activityid = activityid
        self.description = description
        self.regardingobjectid = regardingobjectid
        self.createdon = createdon

class EmailCleaner:
    def __init__(self):
        self.end_keywords = ["Best regards", "best regards", "Sincerely", "Kind regards", "Regards", "Best wishes",
                             "Yours faithfully", "Yours sincerely", "Warm regards", "All the best",
                             "Cheers", "Take care", "Have a nice day", "With appreciation", "Cordially",
                             "Viele Grüße", "Mit freundlichen Grüßen", "Herzliche Grüße", "Liebe Grüße",
                             "Alles Gute", "In freundschaftlicher Verbundenheit", "Hochachtungsvoll",
                             "Beste Wünsche", "Auf Wiedersehen", "Bis bald", "Pass auf dich auf",
                             "Schönen Tag noch", "Mit Dank und besten Grüßen", "Herzlichst", "Liebevoll",
                             "Mit freundlichem Gruß", "Gruß", "Beste Grüße", "LG", "MfG", "Thanks again and best regards"]
        self.patterns = [r"From:.*?Subject:", r"Best regards.*?Subject:", r"Sincerely.*?Subject:",
                         r"Best regards.*?Subject:", r"Kind regards.*?Subject:", r"Regards.*?Subject:",
                         r"Best wishes.*?Subject:", r"Yours faithfully.*?Subject:", r"Yours sincerely.*?Subject:",
                         r"Warm regards.*?Subject:", r"All the best.*?Subject:", r"Cheers.*?Subject:",
                         r"Take care.*?Subject:", r"Have a nice day.*?Subject:", r"With appreciation.*?Subject:",
                         r"Cordially.*?Subject:", r"Viele Grüße.*?Subject:", r"Mit freundlichen Grüßen.*?Subject:",
                         r"Herzliche Grüße.*?Subject:", r"Liebe Grüße.*?Subject:", r"Alles Gute.*?Subject:",
                         r"In freundschaftlicher Verbundenheit.*?Subject:", r"Hochachtungsvoll.*?Subject:",
                         r"Beste Wünsche.*?Subject:", r"Auf Wiedersehen.*?Subject:", r"Bis bald.*?Subject:",
                         r"Pass auf dich auf.*?Subject:", r"Schönen Tag noch.*?Subject:", r"Mit Dank und besten Grüßen.*?Subject:",
                         r"Herzlichst.*?Subject:", r"Liebevoll.*?Subject:", r"Mit freundlichem Gruß.*?Subject:",
                         r"Gruß.*?Subject:", r"Beste Grüße.*?Subject:", r"LG.*?Subject:", r"MfG.*?Subject:",
                         r"Thanks again and best regards.*?Subject:"]
        self.from_to_subject_pattern = r"From:.*?Subject:"
        self.clean_email()

    def remove_html(self, email: Email):
        soup = BeautifulSoup(email.text, 'html.parser')
        email.description = soup.get_text()

    def remove_last_greeting(self, email: Email):
        for keyword in self.end_keywords:
            if keyword in email.description:
                email.description = email.description.split(keyword)[0]

    def remove_greeting_to_subject(self, email: Email):
        for pattern in self.patterns:
            email.description = re.sub(pattern, "", email.description, flags=re.DOTALL)
            email.description = email.description.strip()

    def remove_from_to_subject(self, email: Email):
        email.description = re.sub(self.from_to_subject_pattern, "", email.description, flags=re.DOTALL)
        email.description.strip()

    def clean_email(self, email: Email):
        self.remove_html(email)
        self.remove_greeting_to_subject(email)
        self.remove_from_to_subject(email)
        self.remove_last_greeting(email)
        return email.description

from bs4 import BeautifulSoup
import re
from Email import Email

class PlainTextFromEmailProvider:
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
        

    def remove_html(self, email: Email):
        """
        Remove html tags from email content
        :param email:
        """
        soup = BeautifulSoup(email.content, 'html.parser')
        email.content = soup.get_text()

    def remove_last_greeting(self, email: Email):
        """
        Remove last greeting from email content
        :param email:
        """
        for keyword in self.end_keywords:
            if keyword in email.content:
                email.content = email.content.split(keyword)[0]

    def remove_greeting_to_subject(self, email: Email):
        """
        Remove greeting to subject from email content
        :param email:
        """
        for pattern in self.patterns:
            email.content = re.sub(pattern, "", email.content, flags=re.DOTALL)
            email.content = email.content.strip()

    def remove_from_to_subject(self, email: Email):
        """
        Remove from to subject from email content
        :param email:
        """
        email.content = re.sub(self.from_to_subject_pattern, "", email.content, flags=re.DOTALL)
        email.content.strip()

    def clean_email(self, email: Email):
        """
        Clean email content
        :param email:
        :return email.content: Returns the cleaned email content
        :rtype: str
        """
        self.remove_html(email)
        self.remove_greeting_to_subject(email)
        self.remove_from_to_subject(email)
        self.remove_last_greeting(email)
        return email.content

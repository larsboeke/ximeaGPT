from bs4 import BeautifulSoup
import re

def remove_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    return text

def remove_from_to_subject(text):
    pattern = r"From:.*?Subject:"
    cleaned_text = re.sub(pattern, "", text, flags=re.DOTALL)
    return cleaned_text.strip()


def get_newest_message_from_cleaned_text(text):
    end_keywords = ["Best regards", "Sincerely", "Kind regards", "Regards", "Best wishes", "Yours faithfully",
                      "Yours sincerely", "Warm regards", "All the best", "Cheers", "Take care",
                      "Have a nice day", "With appreciation", "Cordially"]
    for keyword in end_keywords:
        if keyword in text:
            text = text.split(keyword)[0]
    return text

# input is unclean html text with signature
# output is clened text without signatures and other unnecessary stuff
def get_newest_message(text):
    text = remove_html(text)
    text = remove_from_to_subject(text)
    text = get_newest_message_from_cleaned_text(text)
    return text
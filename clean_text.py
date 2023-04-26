from bs4 import BeautifulSoup
import re

def lade_html_datei_als_string(dateipfad):
    with open(dateipfad, 'r', encoding='utf-8') as datei:
        html_inhalt = datei.read()
    return html_inhalt

def extrahiere_text_aus_html(html_inhalt):
    soup = BeautifulSoup(html_inhalt, 'html.parser')
    reiner_text = soup.get_text()
    return reiner_text

def remove_html(text):
    text = extrahiere_text_aus_html(text)
    return text

def remove_from_to_subject(text):
    pattern = r"From:.*?Subject:"
    cleaned_text = re.sub(pattern, "", text, flags=re.DOTALL)
    return cleaned_text.strip()

def remove_text_between_keywords(text):
    start_keywords = ["Best regards", "Sincerely", "Kind regards", "Regards", "Best wishes", "Yours faithfully",
                      "Yours sincerely", "Warm regards", "All the best", "Cheers", "Take care",
                      "Have a nice day", "With appreciation", "Cordially"]
    end_keyword = "From:"
    def replacement(match):
        return match.group(1) + end_keyword
    # Remove every signature except the last one
    regex_pattern = f"({'|'.join(map(re.escape, start_keywords))}).*?{re.escape(end_keyword)}"
    result = re.sub(regex_pattern, replacement, text, flags=re.DOTALL)

    # Remove last signature
    last_start_keyword_regex = f"({'|'.join(map(re.escape, start_keywords))})"
    last_start_keyword_match = re.findall(last_start_keyword_regex, result)

    if last_start_keyword_match:
        last_start_keyword = last_start_keyword_match[-1]
        index = result.rfind(last_start_keyword) + len(last_start_keyword)
        result = result[:index]
    return result

def clean_text(text):
    text = remove_html(text)
    #print("Original ", text)
    #print("Laenge: ", len(text))
    text = remove_text_between_keywords(text)
    text = remove_from_to_subject(text)
    #print("\ngekürzter Text ",text)
    #print("Laenge gekürzt: ", len(text))
    return text

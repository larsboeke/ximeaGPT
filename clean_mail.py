from bs4 import BeautifulSoup

def lade_html_datei_als_string(dateipfad):
    with open(dateipfad, 'r', encoding='utf-8') as datei:
        html_inhalt = datei.read()
    return html_inhalt

def extrahiere_text_aus_html(html_inhalt):
    soup = BeautifulSoup(html_inhalt, 'html.parser')
    reiner_text = soup.get_text()
    return reiner_text

# Ersetzen Sie "beispiel.html" durch den Pfad zu Ihrer HTML-Datei
html_dateipfad = "example_mail.html"
html_inhalt = lade_html_datei_als_string(html_dateipfad)
text = extrahiere_text_aus_html(html_inhalt)

print(text)

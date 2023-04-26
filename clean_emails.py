from clean_mail import clean_text
import csv
csv.field_size_limit(2147483647)

def clean_emails(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
        reader = csv.DictReader(input_file)
        writer = csv.DictWriter(output_file, fieldnames=['description'])
        writer.writeheader()
        for row in reader:
            description = row['Description']
            cleaned_text = clean_text(description)
            writer.writerow({'description': cleaned_text})

clean_emails("emails-case-36517.csv","solution.csv")
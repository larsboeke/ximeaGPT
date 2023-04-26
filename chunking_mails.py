from langchain.text_splitter import RecursiveCharacterTextSplitter
import csv

def read_csv(filename, row_num):
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if i == row_num:
                return str(row['description'])
    return "Zeile nicht gefunden."

def split_text(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                   chunk_overlap=200,
                                                   length_function=len,
                                                   separators='. ')
    chunks = text_splitter.split_text(text)
    return chunks

def chunking_mails(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as input_csvfile, \
            open(output_filename, 'w', encoding='utf-8', newline='') as output_csvfile:

        input_reader = csv.DictReader(input_csvfile)
        fieldnames = ['email_id', 'description']
        output_writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
        output_writer.writeheader()

        email_id = 1
        for row in input_reader:
            description = row['description']
            chunks = split_text(description)

            for chunk in chunks:
                output_writer.writerow({'email_id': email_id, 'description': chunk})

            email_id += 1

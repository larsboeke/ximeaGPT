
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
import csv
def split_csv(filename):
    # Create a new CSV file for the split text
    with open('split_solution.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['E-Mail ID', 'description']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Read the input CSV file row by row
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Split the description field into chunks using the text splitter
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                               chunk_overlap=200,
                                                               length_function=len,
                                                               separators='. ')
                chunks = text_splitter.split_text(row['description'])

                # Write each chunk to the new CSV file with the email ID as reference
                for i, chunk in enumerate(chunks):
                    writer.writerow({'E-Mail ID': row['Email Address'], 'description': chunk})



split_csv('C:/Users/chrii/PycharmProjects/ximeagpt/data/solution.csv')

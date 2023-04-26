import openai
import csv

openai.api_key = "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"
EMBEDDING_MODEL="text-embedding-ada-002"

def add_embeddings_to_csv(input_file_path, output_file_path):

    with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
        reader = csv.DictReader(input_file)
        writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames + ['embeddings'])
        writer.writeheader()

        for row in reader:
            description = row['description']
            embeddings = openai.Embedding.create(input=description, model=EMBEDDING_MODEL)
            row['embeddings'] = embeddings
            writer.writerow(row)


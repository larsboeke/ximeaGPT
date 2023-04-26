from clean_emails import clean_emails
from chunking_mails import chunking_mails
from embedding_emails import add_embeddings_to_csv

email_path = "data/emails-case-36517.csv"
embeddings_path = "data/email_embeddings.csv"

# Clean emails
clean_emails(email_path, "data/solution.csv")
# Chunk emails
chunking_mails("data/solution.csv", "data/solution_chunks.csv")
# Embedd emails
add_embeddings_to_csv("data/solution_chunks.csv",embeddings_path)
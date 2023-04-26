# Email Embedding

This document describes the process of converting emails into embeddings.

## Steps

1. **Parsing HTML Files:** We start by parsing the HTML files into a readable text format without any HTML context. This is done to make the email content easily readable and understandable for the system.

2. **Removing Signatures and Other Information:** After parsing the HTML files, we remove signatures and information such as sender, subject, and receiver, since they are already given in the email and do not provide any additional value to the embedding process.

3. **Chunking Emails:** Once the emails are cleaned, we divide them into chunks and save them in a new file. This step breaks down the email content into smaller, more manageable pieces that can be processed more efficiently.

4. **Converting to Embeddings:** Finally, we convert the email chunks into embeddings or add a new column of embeddings to the CSV file. Embeddings are vector representations of the email content, which can be used to analyze, classify, or compare different emails based on their content.

Overall, this process extracts meaningful information from email content and converts it into a structured format that can be analyzed and processed effectively.

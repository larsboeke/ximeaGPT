#Email Embedding
This document describes the process of converting emails into embeddings. The following steps are involved:

##Parsing HTML Files
The first step is to parse the HTML files into a readable text format without any HTML context. This is done to make the email content easily readable and understandable for the system.

##Removing Signatures and Other Information
After parsing the HTML files, signatures and information such as sender, subject, and receiver are removed. These elements are considered to be already given in the email and do not provide any additional value to the embedding process.

##Chunking Emails
Once the emails are cleaned, they are divided into chunks and saved in a new file. This step is done to break down the email content into smaller, more manageable pieces, which can be processed more efficiently.

##Converting to Embeddings
The final step is to convert the email chunks into embeddings or add a new column of embeddings to the CSV file. Embeddings are vector representations of the email content, which can be used to analyze, classify or compare different emails based on their content.

Overall, this process helps to extract meaningful information from email content and convert it into a structured format that can be analyzed and processed effectively.

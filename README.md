# AI:Lean Project - XIMEA GmbH

Welcome to the AI:Lean project! We aim to revolutionize the way XIMEA GmbH employees interact with corporate data and respond to customer queries using the power of AI. This README provides a comprehensive overview of our project, including its objectives, data model, system architecture, and much more.

## Objective

The project's primary objective is to create an efficient and dependable AI personal assistant that will provide immediate access to a significant portion of the company's internal knowledge base through natural language queries. Our goal is to streamline support request responses and improve overall operational efficiency.

We divide the project requirements into fundamental, high-priority, and mid/low-priority levels to prioritize tasks and ensure optimal delivery. More details on these requirements can be found in our project plan document.

## Data Model

Our team will use two distinct methodologies to prepare the data for the AI chatbot, AI:Lean. 

### Structured Data

For structured data, we will retain the structure of the SQL Database provided by XIMEA. This will be achieved by using a Langchain Tool, designed to interact with the database for efficient information retrieval. We will also adapt to any complexities in the database to ensure optimal functionality.

### Unstructured Data

For unstructured data, we will transform data from emails, manuals, and support tickets into plain text, segment it, and add metadata for context. The segmented plain text will then be stored within a JSON file on a MongoDB server provided by XIMEA and converted into an Embedding Vector on a Pinecone vector database. This approach will ensure the confidentiality and integrity of the data.

We will automate the entire upload process after establishing an optimal chunking size, allowing for a constantly updated chatbot. More details can be found in the data preparation document.

## Datatype

The preparation of the different types of data (emails, manuals, and support tickets) involves various steps for optimal conversion and context. More information on this can be found in the data preparation document.

## System Architecture

### Query Architecture

Our Langchain Agent, powered by an LLM, determines whether to execute a similarity search or access the PDB for each query. The responses are then crafted accordingly for accuracy.

### Databases

#### MongoDB

The MongoDB database is self-hosted inside XIMEA’s office in Muenster, with emails, tickets, and manuals/documentation stored. The index connects the context to the created embeddings in the vector database.

#### Pinecone

Pinecone's Vector database is a cloud-based platform maintained by Pinecone itself. The technical specification of the database will depend on various factors, such as the quantity of chunks, their size, and the database performance required. The vector size will be 1536, as this is the size of the embedding vectors created by OpenAI.

We will determine the most suitable specifications for our needs by conducting cost-performance analyses. We may also consider using different indexes or namespaces within the vector database to enhance its performance.

## Contact

If you have any questions or need further clarification about our project, please feel free to contact us. We are always here to help!

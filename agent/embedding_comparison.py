import openai
import os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")

response = openai.Embedding.create(
    input="Framerate",
    model="text-embedding-ada-002"
)
embeddings = response['data'][0]['embedding']



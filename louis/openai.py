""""Fetch embeddings from the Microsoft Azure OpenAI API"""
import os
import openai


# https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/embeddings?tabs=python

openai.api_type = "azure"
openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_base = "https://cog-f25macgsmc4sm.openai.azure.com"
openai.api_version = "2023-05-15"

def fetch_embedding(tokens):
    """Fetch embedding for a list of tokens from the Microsoft Azure OpenAI API"""
    response = openai.Embedding.create(
        input=tokens,
        engine="ada"
    )
    embeddings = response['data'][0]['embedding']
    return embeddings

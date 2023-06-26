""""Fetch embeddings from the Microsoft Azure OpenAI API"""
import os
import openai
import tiktoken

# https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/embeddings?tabs=python

openai.api_type = "azure"
openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_base = f"https://{os.environ['AZURE_OPENAI_SERVICE']}.openai.azure.com"
openai.api_version = "2023-05-15"

enc = tiktoken.get_encoding("cl100k_base")

def fetch_embedding(tokens):
    """Fetch embedding for a list of tokens from the Microsoft Azure OpenAI API"""
    response = openai.Embedding.create(
        input=tokens,
        engine="ada"
    )
    embeddings = response['data'][0]['embedding']
    return embeddings

# def fetch_tokens_embeddings(text):
#     tokens = get_tokens_from_text(text)
#     embeddings = fetch_embedding(tokens)
#     return (tokens, embeddings)

def get_tokens_from_text(text):
    tokens = enc.encode(text)
    return tokens

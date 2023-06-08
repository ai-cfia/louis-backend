import json

import os

import louis.db as db

CWD = os.path.dirname(os.path.realpath(__file__))

def execute_query(cursor, query):
    # query_embedding = louis.openai.fetch_embedding('what are the cooking temperatures for e.coli?')
    filename = os.path.join(CWD, f"tests/embeddings/{query}.json")
    try:
        with open(filename, encoding='utf-8') as embeddings_file:
            query_embedding = json.loads(embeddings_file.read())
    except FileNotFoundError as file_not_found:
        # query louis.openai for the embedding
        # store it in the filename location
        # pass
        raise file_not_found
    documents = db.match_documents(cursor, query_embedding)
    print(json.dumps(documents, indent=4, ensure_ascii=False))

if __name__ == '__main__':
    connection = db.connect_db()
    with db.cursor(connection) as cursor:
        execute_query(cursor, 'what are the cooking temperatures for e.coli?')
from louis.models import openai
import louis.db as db

def smartsearch(query):
    """Returns list of documents from inspection.canada.ca based on semantic similarity to query"""
    connection = db.connect_db()
    with db.cursor(connection) as cursor:
        documents = db.match_documents_from_text_query(cursor, query)
        return documents[0:5]
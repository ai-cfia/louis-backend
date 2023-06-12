"""The main Flask app for the Louis API."""
import dotenv

from flask import Flask, request, jsonify

from louis import openai
import louis.db as db

dotenv.load_dotenv()

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    """Search for documents similar to the query."""
    query = request.json['query']
    query_embedding = openai.fetch_embedding(query)
    connection = db.connect_db()
    with db.cursor(connection) as cursor:
        documents = db.match_documents(cursor, query_embedding)
        return jsonify(documents)

"""The main Flask app for the Louis API."""
import dotenv

from flask import Flask, request, jsonify

from louis.actions import smartsearch


dotenv.load_dotenv()

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    """Search for documents similar to the query."""
    query = request.json['query']
    return jsonify(smartsearch(query))


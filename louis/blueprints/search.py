"""The main Flask app for the Louis API."""
from flask import Blueprint, request, jsonify

from louis.actions import smartsearch


search = Blueprint('search', __name__)

@search.route('', methods=['POST'])
def search_documents():
    """Search for documents similar to the query."""
    query = request.json['query']
    return jsonify(smartsearch(query))

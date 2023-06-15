import logging

from flask import Blueprint, request, jsonify

from louis.agents.chain import ChainAgent
from louis.agents.louis import Louis
from louis.tools.smartsearch import SmartSearch

chat = Blueprint('chat', __name__)
louis = Louis(SmartSearch)

@chat.route("", methods=["POST"])
def chat_user():
    try:
        r = louis.run(request.json["history"], request.json.get("overrides") or {})
        print(r)
        return jsonify(r)
    except Exception as e:
        logging.exception("Exception in /chat")
        return jsonify({"error": str(e)}), 500

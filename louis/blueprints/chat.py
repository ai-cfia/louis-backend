import logging

from flask import Blueprint, request, jsonify

from louis.agent.chain import ChainAgent
from louis.agent.louis import Louis
from louis.actions import smartsearch

chat = Blueprint('chat', __name__)
louis = Louis(smartsearch)

@chat.route("/", methods=["POST"])
def chat_user():
    try:
        r = louis.run(request.json["history"], request.json.get("overrides") or {})
        return jsonify(r)
    except Exception as e:
        logging.exception("Exception in /chat")
        return jsonify({"error": str(e)}), 500

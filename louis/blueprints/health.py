from flask import Blueprint

health = Blueprint('health', __name__)

@health.route("", methods=["POST"])
def health_user():
    return "ok", 200

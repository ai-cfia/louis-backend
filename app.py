import dotenv

dotenv.load_dotenv()

from flask import Flask

from louis.blueprints.search import search
from louis.blueprints.chat import chat
from louis.blueprints.static import static

app = Flask(__name__, static_folder='static/')

@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def static_file(path):
    return app.send_static_file(path)

app.register_blueprint(search, url_prefix='/search')
app.register_blueprint(chat, url_prefix='/chat')
# app.register_blueprint(static, url_prefix='/', static_folder='dist/')

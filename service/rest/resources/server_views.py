from flask import Blueprint

from service.rest import (app)


server_views = Blueprint('server-views', __name__)


@app.route("/server/ping")
def ping():
    return "Pong!"

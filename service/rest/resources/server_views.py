import os
from flask import Blueprint

from service.rest import (app)


server_views = Blueprint('server-views', __name__)


@server_views.route("/server/ping")
def ping():
    return "Pong!"


@server_views.route("/server/restart", methods = ["POST"])
def restart():
    os.system('sudo reboot')
    return "OK"

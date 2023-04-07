# Run command: flask --app service.rest run --port=4000


from flask import Flask
from flask_cors import CORS


app = Flask(__name__)

CORS(app)

# Make sure this is below the app declaration to ensure not circular imports:
from service.rest.resources.server_views import server_views
from service.rest.resources.cups_views import cups_views


# Register blueprints:
app.register_blueprint(server_views)
app.register_blueprint(cups_views)

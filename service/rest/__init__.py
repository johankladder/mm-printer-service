# Run command: flask --app service.rest run --port=4000


from flask import Flask

app = Flask(__name__)

# Make sure this is below the app declaration to ensure not circular imports:
from service.rest.resources.server_views import server_views

# Blueprints:

# Register blueprints:
app.register_blueprint(server_views)

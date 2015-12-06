
from flask import Flask

from clientapi import client_api


def create_app():
    app = Flask(__name__)
    app.debug = True    

    # blueprints
    app.register_blueprint(client_api)

    return app

# -*- coding: utf-8 -*-

from flask import Flask
import logging

from clientapi import client_api

logger = logging.getLogger(__name__)

coffee_app = Flask(__name__)

coffee_app.register_blueprint(client_api)


@coffee_app.route('/')
def hello():
    return 'Hello World!'


if __name__ == '__main__':

    logger.setLevel(logging.DEBUG)
    coffee_app.run(debug=True, host="0.0.0.0", port=4488)

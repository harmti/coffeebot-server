# -*- coding: utf-8 -*-

from flask import Flask, g

from clientapi import client_api
from process import ProcessData


coffee_app = Flask(__name__)

coffee_app.register_blueprint(client_api)

@coffee_app.before_request
def add_server_to_globals():
    datahandler = ProcessData()
    g.datahandler = datahandler


@coffee_app.route('/')
def hello():
    return 'Hello World!'


if __name__ == '__main__':
    coffee_app.run(debug=True, host="0.0.0.0")

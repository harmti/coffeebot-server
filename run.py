# -*- coding: utf-8 -*-

from app import create_app


coffee_app=create_app()


@coffee_app.route('/')
def hello():
    return 'Hello World!'


if __name__ == '__main__':
    coffee_app.run(debug=True, host="0.0.0.0")

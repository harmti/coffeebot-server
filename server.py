import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/test', methods=['GET', 'POST'])
def test():
    print("request.method:{}".format(request.method))

    return "Hello tester"

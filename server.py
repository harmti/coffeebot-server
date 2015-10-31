import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/test', methods=['GET', 'POST'])
def test():
    print("request.method:{}".format(request.method))
    name=request.form['name']
    return "Hello {}\n".format(name)


@app.route('/v1/post_data', methods=['GET', 'POST'])
def post_data():
    print("/v1/post_data")
    data=request.form['data']
    start=request.form['start']
    end=request.form['end']
    print("start:'{}'".format(start))
    print("end:'{}'".format(end))
    print("data:'{}'".format(data))
    return "Got data:'{}'\n".format(data)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

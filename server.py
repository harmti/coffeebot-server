# -*- coding: utf-8 -*-

import os
from flask import Flask, request

from process import process_data

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
    values=request.form['values']
    start=request.form['start']
    end=request.form['end']
    print("start:{}, end:{}, data:{}".format(start, end, values))

    process_data(values, start, end)
    return "Got data:'{}'\n".format(values)



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

# -*- coding: utf-8 -*-

import os
from flask import Flask, request, Blueprint

from process import process_data

client_api = Blueprint('client_api', __name__)

@client_api.route('/')
def hello():
    return 'Hello World!'

@client_api.route('/helloworld', methods=['GET', 'POST'])
def helloworld():
    print("request.method:{}".format(request.method))
    print(request)
    name=request.form['name']
    return "Hello World!{}\n".format(name)


@client_api.route('/v1/post_data', methods=['GET', 'POST'])
def post_data():
    print("/v1/post_data")
    client_id=request.form['id']
    values=request.form['values']
    start=request.form['start']
    end=request.form['end']
    print("client_id:{}, start:{}, end:{}, values:{}".format(client_id, start, end, values))

    process_data(client_id, values, start, end)
    return "Got data:'{}'\n".format(values)



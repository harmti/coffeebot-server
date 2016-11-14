# -*- coding: utf-8 -*-

import os
from flask import Flask, request, Blueprint

from process import ProcessData

client_api = Blueprint('client_api', __name__)

@client_api.route('/')
def hello():
    return 'Hello World!'

@client_api.route('/v1/post_data', methods=['GET', 'POST'])
def v1_post_data():
    #print("Request: '{}', form:{}".format(request.url, request.form.keys()))
    client_id=request.form['id']
    values=request.form['values']
    start=request.form['start']
    end=request.form['end']
    print("client_id:{}, start:{}, end:{}, values:{}".format(client_id, start, end, values))

    return "Got data:'{}'\n".format(values)



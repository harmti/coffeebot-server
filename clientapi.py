# -*- coding: utf-8 -*-

from flask import request, Blueprint, jsonify
from process import ProcessData
import logging

logger = logging.getLogger(__name__)

client_api = Blueprint('client_api', __name__)

process = ProcessData()

@client_api.route('/')
def hello():
    return 'Greetings from CoffeeBot!'

@client_api.route('/v1/post_data', methods=['GET', 'POST'])
def v1_post_data():
    data = {}
    data['client_id'] = request.form['id']
    data['values'] = request.form['values']
    data['start_time'] = request.form['start']
    data['end_time'] = request.form['end']
    logger.info("data:{}".format(data))

    process.process_data(data)
    return jsonify(data)

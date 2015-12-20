import os
from app import create_app
import pytest
import tempfile
import json

from flask import url_for
from test_init import *


def test_helloworld(app):
    rv = app.get(url_for('client_api.hello'))
    print rv.data
    assert 'Hello' in rv.data

def test_post_data(app):
    values = {"id":"12345678", 
              "start":"Tue Dec  8 18:36:53 EET 2015",
              "end":"Tue Dec  8 18:37:53 EET 2015", 
              "values":"0,0,0,0,0"}
    rv = app.post(url_for('client_api.v1_post_data',values=values))
    #rv = app.post(url_for('client_api.v1_post_data', id="12345678", 
    #                      start="Tue Dec  8 18:36:53 EET 2015",
    #                      end="Tue Dec  8 18:37:53 EET 2015", 
    #                      values="0,0,0,0,0"))
    print rv.data
    assert 'Got data' in rv.data


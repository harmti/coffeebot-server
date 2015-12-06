import os
from app import create_app
import pytest
import tempfile
import json

from flask import url_for
from test_init import *


def test_test(app):
    rv = app.post(url_for('client_api.helloworld'))
    print rv.data
    assert 'Hello' in rv.data


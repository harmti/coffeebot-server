import pytest
import tempfile
import json

from app import create_app

@pytest.fixture(scope='session')
def app(request):

    #class config_override:
    #    TEST_DB_URL = 'sqlite://'
    #    DEBUG = True
    #    TESTING = True

    app = create_app()

    # Establish an application context before running the tests.
    ctx = app.test_request_context()
    #ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app.test_client()


#@pytest.fixture(scope='session')
#def app():
#    app = create_app()
#    return app.test_client()

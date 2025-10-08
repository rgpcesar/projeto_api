import pytest
import json
from app import create_app, db


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()


@pytest.fixture(scope='function')
def auth_token(test_client):
    test_client.post('/users',
                     data=json.dumps(dict(
                         username='testuser',
                         email='test@example.com',
                         password='password'
                     )),
                     content_type='application/json')
    response = test_client.post(
        '/login', auth=('test@example.com', 'password'))
    token = json.loads(response.data)['token']
    return token

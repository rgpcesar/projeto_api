import json
from app import db
from app.models.user_model import User


def test_create_user(test_client):
    """
    GIVEN a Flask application
    WHEN the '/users' page is posted to (POST)
    THEN check that a '201' status code is returned and a new user is created
    """
    response = test_client.post('/users',
                                data=json.dumps(dict(
                                    username='testuser',
                                    email='test@example.com',
                                    password='password'
                                )),
                                content_type='application/json')
    assert response.status_code == 201
    assert b"New user created!" in response.data


def test_create_user_sad_path(test_client):
    """
    GIVEN a Flask application
    WHEN the '/users' page is posted to with missing fields (POST)
    THEN check that a '400' status code is returned
    """
    response = test_client.post('/users',
                                data=json.dumps(dict(
                                    username='testuser'
                                )),
                                content_type='application/json')
    assert response.status_code == 400
    assert b"Missing required fields" in response.data


def test_get_all_users(test_client, auth_token):
    """
    GIVEN a Flask application
    WHEN the '/users' page is requested (GET)
    THEN check that a '200' status code is returned and the users are displayed
    """
    headers = {'x-access-token': auth_token}
    response = test_client.get('/users', headers=headers)
    assert response.status_code == 200
    assert b"testuser" in response.data


def test_get_one_user(test_client, auth_token):
    """
    GIVEN a Flask application
    WHEN the '/users/<user_id>' page is requested (GET)
    THEN check that a '200' status code is returned and the user is displayed
    """
    headers = {'x-access-token': auth_token}
    users_response = test_client.get('/users', headers=headers)
    user_id = json.loads(users_response.data)['users'][0]['id']
    response = test_client.get(f'/users/{user_id}', headers=headers)
    assert response.status_code == 200
    assert b"testuser" in response.data


def test_update_user(test_client, auth_token):
    """
    GIVEN a Flask application
    WHEN the '/users/<user_id>' page is updated (PUT)
    THEN check that a '200' status code is returned and the user is updated
    """
    headers = {'x-access-token': auth_token}
    users_response = test_client.get('/users', headers=headers)
    user_id = json.loads(users_response.data)['users'][0]['id']
    response = test_client.put(f'/users/{user_id}',
                               data=json.dumps(
        dict(username='newusername')),
        content_type='application/json',
        headers=headers)
    assert response.status_code == 200
    assert b"The user has been updated!" in response.data


def test_delete_user(test_client, auth_token):
    """
    GIVEN a Flask application
    WHEN the '/users/<user_id>' page is deleted (DELETE)
    THEN check that a '200' status code is returned and the user is deleted
    """
    headers = {'x-access-token': auth_token}
    users_response = test_client.get('/users', headers=headers)
    user_id = json.loads(users_response.data)['users'][0]['id']
    response = test_client.delete(f'/users/{user_id}', headers=headers)
    assert response.status_code == 200
    assert b"The user has been deleted!" in response.data

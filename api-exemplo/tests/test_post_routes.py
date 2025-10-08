import json
from app import db
from app.models.user_model import User
from app.models.post_model import Post


def test_create_post(test_client, auth_token):
    """
    GIVEN a Flask application and a user
    WHEN the '/posts' page is posted to (POST)
    THEN check that a '201' status code is returned and a new post is created
    """
    headers = {'x-access-token': auth_token}
    response = test_client.post('/posts',
                                data=json.dumps(dict(
                                    title='Test Post',
                                    content='This is a test post.'
                                )),
                                content_type='application/json',
                                headers=headers)
    assert response.status_code == 201
    assert b"New post created!" in response.data


def test_create_post_sad_path(test_client, auth_token):
    """
    GIVEN a Flask application and a user
    WHEN the '/posts' page is posted to with missing fields (POST)
    THEN check that a '400' status code is returned
    """
    headers = {'x-access-token': auth_token}
    # Test missing title
    response = test_client.post('/posts',
                                data=json.dumps(dict(
                                    content='This is a test post.'
                                )),
                                content_type='application/json',
                                headers=headers)
    assert response.status_code == 400
    assert b"Title is required" in response.data
    # Test missing content
    response = test_client.post('/posts',
                                data=json.dumps(dict(
                                    title='Test Post'
                                )),
                                content_type='application/json',
                                headers=headers)
    assert response.status_code == 400
    assert b"Content is required" in response.data
    # Test special characters in title
    response = test_client.post('/posts',
                                data=json.dumps(dict(
                                    title='Test Post!',
                                    content='This is a test post.'
                                )),
                                content_type='application/json',
                                headers=headers)
    assert response.status_code == 400
    assert b"Title cannot contain special characters" in response.data
    # Test no data
    response = test_client.post('/posts',
                                data=json.dumps({}),
                                content_type='application/json',
                                headers=headers)
    assert response.status_code == 400
    assert b"No data provided" in response.data


def test_create_post_no_token(test_client):
    """
    GIVEN a Flask application
    WHEN the '/posts' page is posted to without a token
    THEN check that a '401' status code is returned
    """
    response = test_client.post('/posts',
                                data=json.dumps(dict(
                                    title='Test Post',
                                    content='This is a test post.'
                                )),
                                content_type='application/json')
    assert response.status_code == 401
    assert b"Token is missing!" in response.data


def test_get_all_posts(test_client, auth_token):
    """
    GIVEN a Flask application
    WHEN the '/posts' page is requested (GET)
    THEN check that a '200' status code is returned and the posts are displayed
    """
    headers = {'x-access-token': auth_token}
    test_client.post('/posts',
                     data=json.dumps(dict(
                         title='Test Post',
                         content='This is a test post.'
                     )),
                     content_type='application/json',
                     headers=headers)
    response = test_client.get('/posts')
    assert response.status_code == 200
    assert b"Test Post" in response.data


def test_get_one_post(test_client, auth_token):
    """
    GIVEN a Flask application
    WHEN the '/posts/<post_id>' page is requested (GET)
    THEN check that a '200' status code is returned and the post is displayed
    """
    headers = {'x-access-token': auth_token}
    test_client.post('/posts',
                     data=json.dumps(dict(
                         title='Test Post',
                         content='This is a test post.'
                     )),
                     content_type='application/json',
                     headers=headers)
    posts_response = test_client.get('/posts')
    post_id = json.loads(posts_response.data)['posts'][0]['id']
    response = test_client.get(f'/posts/{post_id}')
    assert response.status_code == 200
    assert b"Test Post" in response.data


def test_update_post(test_client, auth_token):
    """
    GIVEN a Flask application and a user
    WHEN the '/posts/<post_id>' page is updated (PUT)
    THEN check that a '200' status code is returned and the post is updated
    """
    headers = {'x-access-token': auth_token}
    test_client.post('/posts',
                     data=json.dumps(dict(
                         title='Test Post',
                         content='This is a test post.'
                     )),
                     content_type='application/json',
                     headers=headers)
    posts_response = test_client.get('/posts')
    post_id = json.loads(posts_response.data)['posts'][0]['id']
    response = test_client.put(f'/posts/{post_id}',
                               data=json.dumps(dict(title='New Title')),
                               content_type='application/json',
                               headers=headers)
    assert response.status_code == 200
    assert b"The post has been updated!" in response.data


def test_delete_post(test_client, auth_token):
    """
    GIVEN a Flask application and a user
    WHEN the '/posts/<post_id>' page is deleted (DELETE)
    THEN check that a '200' status code is returned and the post is deleted
    """
    headers = {'x-access-token': auth_token}
    test_client.post('/posts',
                     data=json.dumps(dict(
                         title='Test Post',
                         content='This is a test post.'
                     )),
                     content_type='application/json',
                     headers=headers)
    posts_response = test_client.get('/posts')
    post_id = json.loads(posts_response.data)['posts'][0]['id']
    response = test_client.delete(f'/posts/{post_id}', headers=headers)
    assert response.status_code == 200
    assert b"The post has been deleted!" in response.data

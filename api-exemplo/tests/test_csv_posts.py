import json
import csv
import pytest


def get_posts_from_csv():
    with open('tests/posts.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        return [tuple(row) for row in reader]


def create_user_and_post(test_client, username, email, password, title, content):
    # Create user
    test_client.post('/users',
                     data=json.dumps(dict(
                         username=username,
                         email=email,
                         password=password
                     )),
                     content_type='application/json')
    # Login
    response = test_client.post('/login', auth=(email, password))
    token = json.loads(response.data)['token']
    headers = {'x-access-token': token}
    # Create post
    response = test_client.post('/posts',
                                data=json.dumps(dict(
                                    title=title,
                                    content=content
                                )),
                                content_type='application/json',
                                headers=headers)
    posts_response = test_client.get('/posts')
    post_id = [p for p in json.loads(posts_response.data)[
        'posts'] if p['author'] == username and p['title'] == title][0]['id']
    return headers, post_id


@pytest.mark.parametrize("username, email, password, title, content", get_posts_from_csv())
def test_create_posts_from_csv(test_client, username, email, password, title, content):
    """
    GIVEN a Flask application
    WHEN the '/posts' page is posted to with data from a CSV file
    THEN check that a '201' status code is returned and a new post is created
    """
    # Create user
    test_client.post('/users',
                     data=json.dumps(dict(
                         username=username,
                         email=email,
                         password=password
                     )),
                     content_type='application/json')
    # Login
    response = test_client.post('/login', auth=(email, password))
    token = json.loads(response.data)['token']
    headers = {'x-access-token': token}
    # Create post
    response = test_client.post('/posts',
                                data=json.dumps(dict(
                                    title=title,
                                    content=content
                                )),
                                content_type='application/json',
                                headers=headers)

    if not title:
        assert response.status_code == 400
        assert b"Title is required" in response.data
    elif not content:
        assert response.status_code == 400
        assert b"Content is required" in response.data
    elif not all(char.isalnum() or char.isspace() for char in title):
        assert response.status_code == 400
        assert b"Title cannot contain special characters" in response.data
    else:
        assert response.status_code == 201
        assert b"New post created!" in response.data


@pytest.mark.parametrize("username, email, password, title, content", get_posts_from_csv())
def test_update_posts_from_csv(test_client, username, email, password, title, content):
    """
    GIVEN a Flask application
    WHEN a post is updated with data from a CSV file
    THEN check that a '200' status code is returned and the post is updated
    """
    if not title or not content or not all(char.isalnum() or char.isspace() for char in title):
        pytest.skip("Skipping test for invalid post data")

    headers, post_id = create_user_and_post(
        test_client, username, email, password, title, content)
    # Update post
    response = test_client.put(f'/posts/{post_id}',
                               data=json.dumps(dict(
                                   title=f"updated_{title}",
                                   content=f"updated_{content}"
                               )),
                               content_type='application/json',
                               headers=headers)
    assert response.status_code == 200
    assert b"The post has been updated!" in response.data

    # Test updating a non-existent post
    response = test_client.put('/posts/999',
                               data=json.dumps(dict(
                                   title=f"updated_{title}",
                                   content=f"updated_{content}"
                               )),
                               content_type='application/json',
                               headers=headers)
    assert response.status_code == 404
    assert b"Post not found" in response.data


@pytest.mark.parametrize("username, email, password, title, content", get_posts_from_csv())
def test_delete_posts_from_csv(test_client, username, email, password, title, content):
    """
    GIVEN a Flask application
    WHEN a post is deleted
    THEN check that a '200' status code is returned and the post is deleted
    """
    if not title or not content or not all(char.isalnum() or char.isspace() for char in title):
        pytest.skip("Skipping test for invalid post data")

    headers, post_id = create_user_and_post(
        test_client, username, email, password, title, content)
    # Delete post
    response = test_client.delete(f'/posts/{post_id}', headers=headers)
    assert response.status_code == 200
    assert b"The post has been deleted!" in response.data

    # Test deleting a non-existent post
    response = test_client.delete('/posts/999', headers=headers)
    assert response.status_code == 404
    assert b"Post not found" in response.data

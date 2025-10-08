import logging
import allure
import json

log = logging.getLogger(__name__)


@allure.feature("JSONPlaceholder API")
@allure.story("Comments")
def test_get_comments_for_post(api_client):
    """
    Refactored from Aula 2.
    Fetches comments for a specific post and validates them.
    """
    test_name = "test_get_comments_for_post"
    log.info(f"--- Starting test: {test_name} ---")

    post_id = 1
    params = {'postId': post_id}
    url = "https://jsonplaceholder.typicode.com/comments"

    with allure.step(f"Requesting comments for post ID {post_id}"):
        log.info(f"Requesting URL: {url} with params: {params}")
        response = api_client.get(url, params=params)
        log.info(f"Response Status Code: {response.status_code}")
        allure.attach(json.dumps(response.json(), indent=4),
                      name="API Response", attachment_type=allure.attachment_type.JSON)

    with allure.step("Validating response and comments"):
        assert response.status_code == 200
        comments = response.json()
        assert len(comments) > 0
        for comment in comments:
            assert comment['postId'] == post_id

    log.info(f"--- Finished test: {test_name} ---")


@allure.feature("JSONPlaceholder API")
@allure.story("User Todos")
def test_get_completed_todos_for_user(api_client):
    """
    Refactored from Aula 2.
    Fetches completed todos for a specific user.
    """
    test_name = "test_get_completed_todos_for_user"
    log.info(f"--- Starting test: {test_name} ---")

    user_id = 1
    params = {'userId': user_id, 'completed': 'true'}
    url = "https://jsonplaceholder.typicode.com/todos"

    with allure.step(f"Requesting completed todos for user ID {user_id}"):
        log.info(f"Requesting URL: {url} with params: {params}")
        response = api_client.get(url, params=params)
        log.info(f"Response Status Code: {response.status_code}")
        allure.attach(json.dumps(response.json(), indent=4),
                      name="API Response", attachment_type=allure.attachment_type.JSON)

    with allure.step("Validating response and todo status"):
        assert response.status_code == 200
        todos = response.json()
        assert len(todos) > 0
        for todo in todos:
            assert todo['completed'] is True

    log.info(f"--- Finished test: {test_name} ---")

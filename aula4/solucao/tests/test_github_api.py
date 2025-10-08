import logging
import allure
import json

# Get a logger for this module
log = logging.getLogger(__name__)


@allure.feature("GitHub User API")
@allure.story("Fetch user data")
def test_get_specific_user(api_client):
    """
    Refactored test for Exercises 2, 3, 7, 8.
    Fetches a specific user and validates the response.
    """
    test_name = "test_get_specific_user"
    log.info(f"--- Starting test: {test_name} ---")

    username = "octocat"
    url = f"https://api.github.com/users/{username}"

    with allure.step(f"Requesting user '{username}'"):
        log.info(f"Requesting URL: {url}")
        response = api_client.get(url)
        log.info(f"Response Status Code: {response.status_code}")

        # Exercise 8: Attach response to Allure report
        allure.attach(
            json.dumps(response.json(), indent=4),
            name="API Response",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("Validating response"):
        assert response.status_code == 200
        assert response.json()["login"] == username

    log.info(f"--- Finished test: {test_name} ---")


@allure.feature("GitHub Repositories API")
@allure.story("List repositories")
def test_list_user_repositories(api_client):
    """
    Refactored test.
    Lists repositories for a user and validates the count.
    """
    test_name = "test_list_user_repositories"
    log.info(f"--- Starting test: {test_name} ---")

    params = {"per_page": 5}
    url = "https://api.github.com/users/google/repos"

    with allure.step("Requesting repositories for 'google'"):
        log.info(f"Requesting URL: {url} with params: {params}")
        response = api_client.get(url, params=params)
        log.info(f"Response Status Code: {response.status_code}")
        allure.attach(json.dumps(response.json(), indent=4),
                      name="API Response", attachment_type=allure.attachment_type.JSON)

    with allure.step("Validating repository count"):
        assert response.status_code == 200
        assert len(response.json()) == 5

    log.info(f"--- Finished test: {test_name} ---")

# Exercise 5: A test designed to fail to test reporting


@allure.feature("Reporting")
@allure.story("Failure reporting")
def test_failing_for_report_check(api_client):
    """
    This test is designed to fail to demonstrate the reporting hook.
    (For Exercise 10, this test should be deleted or commented out).
    """
    log.info("--- Starting failing test to check report hook ---")
    url = "https://api.github.com/users/nonexistentuser12345"

    with allure.step("Requesting a non-existent user"):
        response = api_client.get(url)
        log.info(f"Response Status Code: {response.status_code}")

    with allure.step("Asserting a failure"):
        # This assertion will fail, triggering the hook in conftest.py
        assert response.status_code == 200

import pytest
import requests
import logging
import json

# Exercise 3: Centralized logging configuration


def setup_logging():
    """Configures logging to file and console."""
    logging.basicConfig(
        level=logging.DEBUG,  # Set the lowest level to capture all messages
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.FileHandler("test_run.log", mode='w'),
            logging.StreamHandler()
        ]
    )


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """Hook to set up logging once before any tests run."""
    setup_logging()

# Exercise 2 & 6: Centralized API client fixture


class ApiClient(requests.Session):
    """A custom requests.Session to store the last response."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_response = None

    def request(self, method, url, *args, **kwargs):
        """Override request to store the last response."""
        response = super().request(method, url, *args, **kwargs)
        self.last_response = response
        return response


@pytest.fixture(scope="session")
def api_client():
    """
    Fixture that provides an instance of our custom ApiClient.
    Using "session" scope means it's created once for the entire test run.
    """
    yield ApiClient()

# Exercise 6: Hook to add response body to failed test reports


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test outcome and add extra info to the report.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        # Try to get the api_client fixture from the test item
        if 'api_client' in item.fixturenames:
            client = item.funcargs['api_client']
            last_response = getattr(client, 'last_response', None)

            if last_response:
                # Add a section to the HTML report
                report.longrepr.addsection(
                    'API Response Body',
                    json.dumps(last_response.json(), indent=4),
                    blue=True
                )

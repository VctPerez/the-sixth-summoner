import pytest

from utils.logging import setup_logging

@pytest.fixture(scope="session", autouse=True)
def configure_test_logging():
    setup_logging()
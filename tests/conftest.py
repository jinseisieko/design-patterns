"""Pytest configuration and fixtures."""

import pytest

from app import create_app


@pytest.fixture
def app():
    """Create Flask application for testing.

    Yields:
        Flask application instance.
    """
    app = create_app("testing")
    yield app


@pytest.fixture
def client(app):
    """Create test client.

    Args:
        app: Flask application.

    Yields:
        Flask test client.
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create CLI runner.

    Args:
        app: Flask application.

    Yields:
        Flask CLI runner.
    """
    return app.test_cli_runner()

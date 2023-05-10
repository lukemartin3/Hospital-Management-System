import pytest
from src.app import run_app

@pytest.fixture()
def app():
    app = run_app()
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

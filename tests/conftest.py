import pytest

from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        print('test', client)
        yield client
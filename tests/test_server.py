from tests.conftest import client


def test_index(client):
    """
    Testing the index route
    :param client: pytest fixture providing a mock Flask test client
    """
    response = client.get('/')
    assert response.status_code == 200
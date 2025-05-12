from unittest.mock import patch
from tests.conftest import client, data_mock

def test_show_summary(client, data_mock, loaded_clubs, loaded_competitions):
    def test_show_summary(client, data_mock, loaded_clubs, loaded_competitions):
        """
        Test the 'show_summary' route by simulating a POST request with a valid email.
        - Checks that the provided email exists in the list of clubs.
        - Verifies that the clubs and competitions are loaded correctly.
        - Ensures that the status code of the response is 200.
        - Confirms that the response content type is 'text/html; charset=utf-8'.
        - Asserts that the loaded clubs and competitions match the provided mock data.
        """
    with patch('server.load_clubs', return_value=data_mock['clubs']), \
            patch('server.load_competitions', return_value=data_mock['competitions']):

            assert len(data_mock['clubs']) > 0
            assert len(data_mock['competitions']) > 0

            email = data_mock['clubs'][0]['email']
            assert email == "a@example.com", f"L'email n'est pas valide"

            response = client.post('/showSummary', data={
                'email': email,
            })

            assert response.status_code == 200, f"Le code de statut de la réponse attendu est 200, mais reçu {response.status_code}"
            assert response.content_type == 'text/html; charset=utf-8'

            assert loaded_clubs == data_mock['clubs']
            assert loaded_competitions == data_mock['competitions']

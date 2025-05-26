from tests.conftest import client, data_mock

def test_show_summary(client, data_mock):
        # Test pour verifier si un club ou une competiton existe
        assert len(data_mock['clubs']) > 0
        assert len(data_mock['competitions']) > 0

        # Aucun email envoyé
        response = client.post('/showSummary', data={})
        assert response.status_code == 400

        # Email valide
        email = data_mock['clubs'][0]['email']
        response = client.post('/showSummary', data={'email': email})
        assert response.status_code == 200

        # Email invalide
        invalid_email = "invalid@example.com"
        response = client.post('/showSummary', data={'email': invalid_email})
        assert response.status_code == 400
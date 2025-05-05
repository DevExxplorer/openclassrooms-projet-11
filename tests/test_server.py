from unittest.mock import patch

from tests.conftest import client, data_mock

def test_index(client):
    """
    Testing the index route
    :param client: pytest fixture providing a mock Flask test client
    """
    response = client.get('/')
    assert response.status_code == 200


def test_purchase_places(client, data_mock):
    with patch('server.load_clubs', return_value=data_mock['club']), \
            patch('server.load_competitions', return_value=data_mock['competition']):

            club = data_mock['club'][0]
            competition = data_mock['competition'][0]
            places =  data_mock['places']

            response = client.post('/purchasePlaces', data={
                'club': club['name'],
                'competition': competition['name'],
                'places': places,
            })

            assert isinstance(places, int), f"La valeur de places doit être un entier"
            assert 0 < places <= 12, f"Le nombre de places doit être entre 1 à 12"

            # number_of_places_in_competition = int(competition['numberOfPlaces'])
            # assert int(number_of_places_in_competition) - places == 20, f"le résultat est incorrect"

            assert response.status_code == 200, f"Le code de statut de la réponse attendu est 200, mais reçu {response.status_code}"


def test_show_summary(client, data_mock):
    with patch('server.load_clubs', return_value=data_mock['club']), \
            patch('server.load_competitions', return_value=data_mock['competition']):

            # check if competition and club exists
            assert len(data_mock['club']) > 0
            assert len(data_mock['competition']) > 0

            # check if email is valid

            email = data_mock['club'][0]['email']
            assert email == "test@club.com", f"L'email n'est pas valide"

            # check if status code is 200

            response = client.post('/showSummary', data={
                'email': email,
            })

            assert response.status_code == 200, f"Le code de statut de la réponse attendu est 200, mais reçu {response.status_code}"
            assert response.content_type == 'text/html; charset=utf-8'

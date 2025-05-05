from unittest.mock import patch

from server import load_clubs, load_competitions
from tests.conftest import client, mock_clubs_and_competitions

def test_index(client):
    """
    Testing the index route
    :param client: pytest fixture providing a mock Flask test client
    """
    response = client.get('/')
    assert response.status_code == 200


def test_purchase_places(client, mock_clubs_and_competitions):
    with patch('server.load_clubs', return_value=mock_clubs_and_competitions['club']), \
            patch('server.load_competitions', return_value=mock_clubs_and_competitions['competition']):

            club = mock_clubs_and_competitions['club'][0]
            competition = mock_clubs_and_competitions['competition'][0]
            places =  mock_clubs_and_competitions['places']

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

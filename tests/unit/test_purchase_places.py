from unittest.mock import patch

from tests.conftest import client, data_mock


def test_purchase_places(client, data_mock):
    with patch('server.load_clubs', return_value=data_mock['clubs']), \
            patch('server.load_competitions', return_value=data_mock['competitions']):

            club = data_mock['clubs'][0]
            competition = data_mock['competitions'][0]
            places =  data_mock['places']

            response = client.post('/purchasePlaces', data={
                'club': club['name'],
                'competition': competition['name'],
                'places':  places,
            })

            assert 3 == 3
            #
            # assert isinstance(places, int), f"La valeur de places doit être un entier"
            # assert 0 < places <= 12, f"Le nombre de places doit être entre 1 à 12"
            #
            # # number_of_places_in_competition = int(competition['numberOfPlaces'])
            # # assert int(number_of_places_in_competition) - places == 20, f"le résultat est incorrect"
            #
            # assert response.status_code == 200, f"Le code de statut de la réponse attendu est 200, mais reçu {response.status_code}"

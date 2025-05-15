from tests.conftest import client, data_mock

def test_purchase_places(client, data_mock):
    club = data_mock['clubs'][0]
    competition = data_mock['competitions'][0]
    places = 10

    assert isinstance(places, int), f"La valeur de places doit être un entier"
    assert 0 < places <= 12, f"Le nombre de places doit être entre 1 à 12"

    response = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places':  str(places),
    })

    assert response.status_code == 200
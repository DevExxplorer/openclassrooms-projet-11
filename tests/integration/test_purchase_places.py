from tests.conftest import client, data_mock

def test_purchase_places(client, data_mock):
    # Test avec données valides
    club = data_mock['clubs'][0]
    competition = data_mock['competitions'][0]
    places = 10

    response = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places':  str(places),
    })

    assert response.status_code == 200

    # Test avec données valides et places invalides pour gérer le try
    response = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places': 'invalid',
    })
    assert response.status_code == 200


    # Test avec données invalides et places valides
    response = client.post('/purchasePlaces', data={
        'club': 'ClubInconnu',
        'competition': 'CompetitionInconnu',
        'places': '10',
    })

    assert response.status_code == 400


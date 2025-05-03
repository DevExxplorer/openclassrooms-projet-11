from server import load_competitions, load_clubs
from tests.conftest import client

def test_index(client):
    """
    Testing the index route
    :param client: pytest fixture providing a mock Flask test client
    """
    response = client.get('/')
    assert response.status_code == 200


def test_purchase_places(client):
    competitions = load_competitions()
    clubs = load_clubs()

    data = {
        'club': clubs[0]['name'],
        'competition': competitions[0]['name'],
        'places': 5
    }
    response = client.post('/purchasePlaces', data=data)

    # Verifie que j'ai un code 200 et pas un autre
    assert response.status_code == 200, f"Le code de statut de la réponse attendu est 200, mais reçu {response.status_code}"

    # Verifie que c'est bien un nombre entier
    assert isinstance(data['places'], int), f"La valeur de places doit être un entier"

    # Verifie que le nombre est entre 1 et 12.
    assert 0 < data['places'] <= 12, f"Le nombre de places doit être entre 1 à 12"

    # Vérifie que les clubs et competitions existent bien
    check_is_data_json_exist(competitions, data['competition'])
    check_is_data_json_exist(clubs, data['club'])

    # Verifie que l'affichage du résultat soit le bon
    number_of_places_in_competition = int(competitions[0]['numberOfPlaces'])
    assert number_of_places_in_competition - data['places'] == 20, f"le résultat est incorrect"

def check_is_data_json_exist(json_data, research):
    found = False

    for item in json_data:
        if item['name'] == research:
            found = True
            break

    if not found:
        raise AssertionError(f"Erreur : L'élément recherché n'existe pas.")

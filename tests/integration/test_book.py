from tests.conftest import client, data_mock

def test_book(client, data_mock):
    """
       Teste la route '/book/<competition>/<club>' pour différents cas.

       Vérifie que la page de réservation est accessible (code 200)
       lorsque la compétition et le club existent, et que la réponse
       renvoie un code 400 (erreur) lorsque la compétition ou le club
       n'existent pas.

       Args:
           client (FlaskClient): Client de test Flask simulant les requêtes HTTP.
           data_mock (dict): Données factices contenant 'clubs' et 'competitions'.

       Assertions:
           - Code 200 si compétition et club valides.
           - Code 400 si compétition ou club invalides.
       """
    clubs = data_mock["clubs"]
    competitions = data_mock["competitions"]

    # Test si competition et club sont valides
    response = client.get(f'/book/{competitions[0]["name"]}/{clubs[0]["name"]}')
    assert response.status_code == 200

    # Test si competition est invalide
    response = client.get(f'/book/NoCompetition/{clubs[0]["name"]}')
    assert response.status_code == 400

    # Test si club est invalide
    response = client.get(f'/book/{competitions[0]["name"]}/NoClub')
    assert response.status_code == 400

    # Test si club et competition sont invalides
    response = client.get(f'/book/NoCompetition/NoClub')
    assert response.status_code == 400
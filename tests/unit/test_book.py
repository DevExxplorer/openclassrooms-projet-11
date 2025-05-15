from tests.conftest import client, data_mock

def test_book(client, data_mock):
    clubs = data_mock["clubs"]
    competitions = data_mock["competitions"]

    # Test si competition et club sont valides
    response = client.get(f'/book/{competitions[0]["name"]}/{clubs[0]["name"]}')
    assert response.status_code == 200

    # Test si competition est invalide
    response = client.get(f'/book/NoCompetition/{clubs[0]["name"]}')
    assert response.status_code == 302

    # Test si club est invalide
    response = client.get(f'/book/{competitions[0]["name"]}/NoClub')
    assert response.status_code == 302

    # Test si club et competition sont invalides
    response = client.get(f'/book/NoCompetition/NoClub')
    assert response.status_code == 302
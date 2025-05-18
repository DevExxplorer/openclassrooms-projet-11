import server
import pytest


def test_load_clubs(data_mock, patch_data):
    """
       Teste que la liste des clubs dans le module server correspond bien aux données mockées.

       - Vérifie que la liste initiale des clubs est conforme à data_mock["clubs"].
       - Ajoute un club invalide et vérifie que la comparaison échoue,
         ce qui doit lever une AssertionError.

       Args:
           data_mock (dict): Données simulées contenant la liste des clubs attendus.
           patch_data: Fixture ou mécanisme pour patcher/modifier les données (non utilisé explicitement ici).

       Raises:
           AssertionError: Si la liste des clubs ne correspond pas aux données mockées.
       """

    # Test si valide
    assert server.clubs == data_mock["clubs"]

    # Test si invalide
    server.clubs.append({"name": "Erreur", "email": "error@example.com", "points": "0"})
    with pytest.raises(AssertionError):
        assert server.clubs == data_mock["clubs"]
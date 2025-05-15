import server
import pytest

def test_load_competitions(data_mock, patch_data):
    """
    Teste que la liste des compétitions dans le module server correspond bien aux données mockées.

    - Vérifie que la liste initiale des compétitions est conforme à data_mock["competitions"].
    - Ajoute une compétition invalide et vérifie que la comparaison échoue,
      ce qui doit lever une AssertionError.

    Args:
        data_mock (dict): Données simulées contenant la liste des compétitions attendues.
        patch_data: Fixture ou mécanisme pour patcher/modifier les données (non utilisé explicitement ici).

    Raises:
        AssertionError: Si la liste des compétitions ne correspond pas aux données mockées.
    """

    # Test si valide
    assert server.competitions == data_mock["competitions"]

    # Test si invalide
    server.competitions.append({"name": "CompetitionInconnu", "date": "2026-03-27 10:00:00", "numberOfPlaces": "20"})
    with pytest.raises(AssertionError):
        assert server.competitions == data_mock["competitions"]
import pytest
from server import validate_places

def test_validate_places():
    """
    Teste la fonction `validate_places` avec les nouveaux paramètres.

    - Vérifie qu'une valeur valide (par exemple 5) est acceptée.
    - Vérifie que des valeurs invalides lèvent une ValueError :
      * pas un entier
      * hors bornes (0, 13)
      * plus grand que competition_places
      * plus grand que club_points
    """

    competition_places = 10
    club_points = 8

    # Cas valide : places = 5, qui est <= competition_places et <= club_points
    validate_places(5, competition_places, club_points)

    # Cas invalides type ou bornes
    invalid_places_list = [0, 13, "cinq", None]
    for invalid_place in invalid_places_list:
        with pytest.raises(ValueError):
            validate_places(invalid_place, competition_places, club_points)

    # Cas invalides dépassement competition_places
    with pytest.raises(ValueError):
        validate_places(11, competition_places, club_points)

    # Cas invalides dépassement club_points
    with pytest.raises(ValueError):
        validate_places(9, competition_places, club_points)

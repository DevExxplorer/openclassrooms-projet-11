import pytest
from server import validate_places, club_bookings

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
    club_name = "Test Club"
    competition_name = "Test Competition"

    # Nettoyer les données de test précédentes
    club_bookings.pop(club_name, None)

    # Cas valide : places = 5, qui est <= competition_places et <= club_points
    validate_places(5, competition_places, club_points, club_name, competition_name)

    # Cas invalides type ou bornes
    invalid_places_list = [0, 13, "cinq", None]
    for invalid_place in invalid_places_list:
        with pytest.raises(ValueError):
            validate_places(invalid_place, competition_places, club_points, club_name, competition_name)

    # Cas invalides dépassement competition_places
    with pytest.raises(ValueError):
        validate_places(11, competition_places, club_points, club_name, competition_name)

    # Cas invalides dépassement club_points
    with pytest.raises(ValueError):
        validate_places(9, competition_places, club_points, club_name, competition_name)

def test_validate_places_booking_limit():
    """
    Teste  la limitation de 12 places par club par tournoi.
    """
    competition_places = 25
    club_points = 20
    club_name = "Test Club Limit"
    competition_name = "Test Competition Limit"

    # Nettoyer les données de test précédentes
    club_bookings.pop(club_name, None)

    # Simuler qu'il y a déjà 8 places réservées
    club_bookings[club_name] = {competition_name: 8}

    # Cas valide : réserver 4 places de plus (total = 12)
    validate_places(4, competition_places, club_points, club_name, competition_name)

    # Cas invalide : essayer de réserver 5 places de plus (total = 13 > 12)
    with pytest.raises(ValueError, match="Vous ne pouvez réserver que 4 place"):
        validate_places(5, competition_places, club_points, club_name, competition_name)

    # Simuler qu'il y a déjà 12 places réservées
    club_bookings[club_name][competition_name] = 12

    # Cas invalide : essayer de réserver 1 place de plus quand déjà au maximum
    with pytest.raises(ValueError, match="Vous avez déjà réservé le maximum"):
        validate_places(1, competition_places, club_points, club_name, competition_name)

    # Nettoyer après le test
    if club_name in club_bookings:
        del club_bookings[club_name]
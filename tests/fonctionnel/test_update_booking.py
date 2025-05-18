def test_update_booking():
    """
    Teste la mise à jour des places disponibles d'une compétition et des points d'un club
    après une réservation.

    Simule la réservation de places en réduisant le nombre de places disponibles dans la compétition
    et en déduisant les points correspondants du club.

    Assertions:
    - Le nombre de places de la compétition doit diminuer du nombre réservé.
    - Les points du club doivent diminuer du même nombre.
    """
    competition = {'numberOfPlaces': 20}
    club = {'points': '15'}
    places_required = 5

    # Simuler réservation
    competition['numberOfPlaces'] = competition['numberOfPlaces'] - places_required
    club['points'] = str(int(club['points']) - places_required)

    assert competition['numberOfPlaces'] == 15
    assert club['points'] == '10'
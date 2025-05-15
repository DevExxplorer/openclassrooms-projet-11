from server import find_club_by_email

def test_find_club_by_email(data_mock):
    """
    Teste la fonction find_club_by_email.

    Vérifie que la fonction retourne bien le club correspondant à un email existant
    et retourne None si l'email n'existe pas dans la liste des clubs.

    Args:
        data_mock (dict): Données factices contenant une liste de clubs sous la clé 'clubs'.
    """
    clubs = data_mock['clubs']

    # Email existant
    email = clubs[0]['email']
    club = find_club_by_email(email, clubs)
    assert club is not None
    assert club['email'] == email

    # Email inexistant
    club = find_club_by_email('inexistant@example.com', clubs)
    assert club is None
def test_index(client):
    """
    Teste la route racine '/' pour s'assurer qu'elle répond correctement.

    - Envoie une requête GET sur la page d'accueil.
    - Vérifie que la réponse a un code HTTP 200 (OK).
    - Vérifie que le type de contenu de la réponse est 'text/html; charset=utf-8'.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'

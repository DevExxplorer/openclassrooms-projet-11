def test_logout(client):
    """
    Teste la route '/logout' en vérifiant que la redirection fonctionne correctement.

    - Envoie une requête GET sur '/logout'.
    - Vérifie que la réponse a un code HTTP 302 (redirection).
    """
    response = client.get('/logout')
    assert response.status_code == 302

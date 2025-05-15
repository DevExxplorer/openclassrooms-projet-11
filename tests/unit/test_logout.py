def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302
    assert response.content_type == 'text/html; charset=utf-8'




def test_register(client):
    response = client.get('/register')
    assert b"<title> Register </title>" in response.data


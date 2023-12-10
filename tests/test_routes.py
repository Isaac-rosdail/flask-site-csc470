
def test_home(client):
    response = client.get('/')
    assert b"<title> Home </title>" in response.data

def test_register(client):
    response = client.get('/register')
    assert b"<title> Register </title>" in response.data


from app.app import User

# Ensure returns data.json file
def test_data_json(client):
    response = client.get('/api/data')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'


# Test that register function adds user to db
def test_registration(client, app_ctx):
    with app_ctx.app_context():
        form_data = {
            "name": "Test Name",
            "username": "testUsername",
            "email": "testEmail",
            "password": "testPassword",
            "role": "0",
            "dept": "0"
        }
        response = client.post('/register', data=form_data, follow_redirects=True)

        assert User.query.count() == 1
        user = User.query.first()
        assert user.username == "testUsername"

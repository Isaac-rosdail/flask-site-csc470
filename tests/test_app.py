from app.app import User


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

from app.app import User, create_default_admin

# Ensure returns data.json file
def test_data_json(client):
    response = client.get('/api/data')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

def test_create_default_admin(client, app_ctx):
    create_default_admin()

    admin = User.query.filter_by(username='admin.account').first()
    assert admin is not None
    assert admin.username == 'admin.account'
    assert admin.email == 'admin.account@corn.com'
    assert admin.role == 'admin'
    assert admin.dept == 'IT'


# Test that register function adds user to db
def test_create_user(client, app_ctx):
    with app_ctx.app_context():
        form_data = {
            "name": "testName",
            "username": "test.user1",
            "email": "test.user1@corn.com",
            "password": "TestPass1!",
            "dept": "HR",
        }
        response = client.post('/register', data=form_data, follow_redirects=True)

        # Check response
        assert response.status_code == 200

        assert User.query.count() == 1
        user = User.query.first()
        assert user.username == "test.user1"
        assert user.email == 'test.user1@corn.com'

from flask import url_for
from app.app import User, Ticket, create_default_admin, filter_tickets, db
from unittest.mock import patch
from flask_login import current_user

# Ensure returns data.json file
def test_data_json(client):
    response = client.get('/api/data')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'


# Test user registration
def test_user_registration(client, app_ctx):
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
        # Commit changes
        db.session.commit()

        assert User.query.count() == 1
        user = User.query.first()
        assert user.username == "test.user1"
        assert user.email == 'test.user1@corn.com'


# Test user login
def test_valid_user_login(client, app_ctx):

    login_data = {
        'username': 'valid.user1',
        'password': 'hashCorn1!'
    }
    response = client.post('/', data=login_data, follow_redirects=True)

    assert response.status_code == 200
    assert b'Invalid username or password' not in response.data


def test_invalid_user_login(client, app_ctx):

    login_data = {
        'username': 'invalid.user1',
        'password': 'wrongPassword1!'
    }
    response = client.post('/', data=login_data, follow_redirects=True)

    assert response.status_code == 200

    with app_ctx.app_context():
        assert current_user.is_authenticated
        assert current_user.is_anonymous


# Test user logout
def test_logout(client, app_ctx, login):
    response = client.get(url_for('logout'), follow_redirects=True)

    # Check if response redirects to home route
    assert response.status_code == 200
    assert b'Log in' in response.data


# Test create default admin
def test_create_default_admin(client, app_ctx):
    create_default_admin()

    admin = User.query.filter_by(username='admin.account').first()
    assert admin is not None
    assert admin.username == 'admin.account'
    assert admin.email == 'admin.account@corn.com'
    assert admin.role == 'admin'
    assert admin.dept == 'IT'


# Test edit user functionality
def test_edit_user(client, app_ctx):
    user_id = 1
    edit_data = {
        'name': 'New Name',
        'username': 'new.username1',
        'email': 'new.email1@corn.com',
        'dept': 'HR',
    }
    response = client.post(f'/edit_user/{user_id}', data=edit_data, follow_redirects=True)

    assert response.status_code == 200
    # Add more assertions here to verify the user data was actually updated
    updated_user = User.query.get(user_id)
    assert updated_user is not None
    assert updated_user.username == 'new.username1'
    assert updated_user.email == 'new.email1@corn.com'
    assert updated_user.dept == 'HR'


# Test user deletion
def test_delete_user(client, app_ctx):
    user_id = 1
    response = client.post(f'/delete_user/{user_id}', follow_redirects=True)

    assert response.status_code == 200
    deleted_user = User.query.get(user_id)
    assert deleted_user is None


# Test ticket submission
def test_submit_ticket(client, app_ctx):
    ticket_data = {
        'created_by': 'example_user',
        'dept': '1',  # Assuming '1' corresponds to 'HR'
        'title': 'Test Ticket',
        'assigned_to': 'admin',
        'status': 'open',
        'priority': 'low',
        'description': 'Test Description',
        'location': 'office1',
        'attachment': 'test_attachment.jpg'
    }
    response = client.post('/submit_ticket', data=ticket_data, follow_redirects=True)

    assert response.status_code == 200
    new_ticket = Ticket.query.filter_by(title='Test Ticket').first()
    # assert new_ticket is not None
    assert new_ticket.dept == '1'
    assert new_ticket.assigned_to == 'admin'
    assert new_ticket.status == 'open'
    assert new_ticket.priority == 'low'
    assert new_ticket.location == 'office1'
    assert new_ticket.attachment == 'test_attachment.jpg'

# Test ticket editing


# Test ticket deletion

# Test ticket viewing

# Test ticket filtering & sorting
def test_tickets_functions(client, app_ctx):
    with app_ctx.app_context():

        # Set up test data
        hashed_password = 'hash_corn1!'
        user1 = User(username='example_user1', password=hashed_password, role='user', dept='HR')
        user2 = User(username='example_user2', password=hashed_password, role='admin', dept='IT')
        db.session.add_all([user1, user2])

        # Adding multiple tickets
        for i in range(10):
            ticket = Ticket(created_by='example_user1', assigned_to=f'assignee_{i}', dept='HR')
            db.session.add(ticket)
        db.session.commit()

        # Set current_user using mock
        with patch('flask_login.utils._get_user') as current_user_mock:
            current_user_mock.return_value = user2

            # Test filtering by 'created'
            tickets = filter_tickets('example_user1', 'created')
            assert len(tickets) == 10
            for ticket in tickets:
                assert ticket.created_by == 'example_user1'

            # Test default filtering for admin (i.e., return all tickets)
            tickets = filter_tickets('example_user2', 'all')
            assert len(tickets) == 10

# Test form validation (for RegisterForm, LoginForm, TicketForm, EditUserForm)

# Test protected routes (login required)

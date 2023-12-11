from app.app import User, Ticket, create_default_admin, filter_tickets, db
from flask_paginate import Pagination
from unittest.mock import patch

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

            # Tests pagination
            PER_PAGE = 5
            response = client.get('/tickets?page=1')
            assert len(response.json) == PER_PAGE

            response = client.get('/tickets?page=2')
            assert len(response.json) == (10 - PER_PAGE)
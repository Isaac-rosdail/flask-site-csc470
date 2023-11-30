# Used to set up testing env and get things to be called before every test
import pytest
from app.app import app, db

@pytest.fixture()
def app():
    # Everything that happens before running a test
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()  # Allows us to simulate requests to the app

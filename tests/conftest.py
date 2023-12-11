# Used to set up testing env and get things to be called before every test
import pytest
from app.app import app as flask_app, db, User  # Renamed to avoid conflict


@pytest.fixture()
def app_ctx():  # Renamed the fixture
    # Everything that happens before running a test
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['SECRET_KEY'] = 'test_secret_key'  # Secret key for testing
    flask_app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF token for testing

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app_ctx):  # Use the renamed fixture here
    return app_ctx.test_client()  # Allows us to simulate requests to the app

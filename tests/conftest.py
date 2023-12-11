# Used to set up testing env and get things to be called before every test
import pytest
from werkzeug.security import generate_password_hash
from app.app import app as flask_app, db, User  # Renamed to avoid conflict
from flask_login import login_user

@pytest.fixture()
def app_ctx():  # Renamed the fixture
    # Everything that happens before running a test
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['SECRET_KEY'] = 'test_secret_key'  # Secret key for testing
    flask_app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF token for testing
    flask_app.config['SERVER_NAME'] = 'localhost:5000'
    flask_app.config['APPLICATION_ROOT'] = '/'

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app_ctx):  # Use the renamed fixture here
    return app_ctx.test_client()  # Allows us to simulate requests to the app

@pytest.fixture()
def login(client, app_ctx):
    with app_ctx.app_context():
        # Create test user & add to database
        hashed_password = generate_password_hash('hashCorn1!', method='pbkdf2:sha256')
        user = User(name='Test user', username='test.user1', password=hashed_password, email='test.user1@corn.com', dept='IT')
        db.session.add(user)
        db.session.commit()

        return user


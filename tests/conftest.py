import pytest

from app import create_app
from app.extensions import db
from app.models import User


@pytest.fixture()
def app(tmp_path):
    database_path = tmp_path / "test.db"
    app = create_app(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": False,
            "SECRET_KEY": "test-key",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path}",
        }
    )
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User(name="Ana", email="ana@example.com")
        user.set_password("123456")
        other = User(name="Bruno", email="bruno@example.com")
        other.set_password("123456")
        db.session.add_all([user, other])
        db.session.commit()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def login(client):
    def do_login(email="ana@example.com", password="123456"):
        return client.post(
            "/auth/login", data={"email": email, "password": password}, follow_redirects=True
        )
    return do_login

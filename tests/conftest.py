import pytest
from api_best_cars import create_app, db
from api_best_cars.models import User


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )
    with app.app_context():
        #db.create_all()
        db.metadata.create_all(bind=db.engine)

        yield app

        # db.drop_all()
        db.metadata.drop_all(bind=db.engine)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def admin():
    admin = User(
        name="admin",
        email="admin@admin.admin",
        psw="admin",
        admin=True,
    )
    db.session.add(admin)
    db.session.commit()
    return admin


@pytest.fixture(scope="session")
def user():
    user = User(
        name="user",
        email="user@user.user",
        psw="user",
        admin=False,
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture()
def admin_token(client, admin):
    res = client.post(
        "/login",
        json={
            "email": admin.email,
            "psw": "admin",
        },
    )
    token = res.get_json()["message"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers


@pytest.fixture()
def user_token(client, user):
    res = client.post(
        "/login",
        json={
            "email": user.email,
            "psw": "user",
        },
    )
    token = res.get_json()["message"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

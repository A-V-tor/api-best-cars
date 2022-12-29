from werkzeug.security import check_password_hash


def test_register(client):
    res = client.post(
        "/register",
        json={"name": "test", "email": "test@test.test", "psw": "test", "admin": True},
    )

    assert res.status_code == 200
    assert len(res.get_json()["message"]) > 10


def test_login(admin, client):
    assert admin.name == "admin"
    assert check_password_hash(admin.psw, "admin")

    res = client.post("/login", json={"email": admin.email, "psw": "admin"})

    assert res.get_json().get("message")

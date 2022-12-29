def test_send_data_admin(client, admin_token):
    res = client.post(
        "/",
        json={
            "brend": "Ford",
            "model": "Model T",
            "year": 1908,
            "engine": "cumbustion",
            "max_speed": 72,
            "released_copies": "over 15 million",
            "description": "Ford Model T стал первым массовым автомобилем.",
        },
        headers=admin_token,
    )

    assert res.status_code == 200

    res = client.post(
        "/",
        json={
            "brend": "Dodge Brothers",
            "model": "Model 30",
            "year": 1919,
            "engine": "cumbustion",
            "max_speed": 80,
            "released_copies": "116 400 copies",
            "description": "Автомобиль имел рядный четырехцилиндровый двигатель с L-образной головкой рабочим объемом 212 кубических дюймов (3,5 л) и выходной мощностью 35 л.с. (25,7 кВт).",
        },
        headers=admin_token,
    )

    assert res.status_code == 200

    res = client.post(
        "/",
        json={
            "brend": "Detroit Electric",
            "model": "Detroit Electric",
            "year": 1920,
            "engine": "electric",
            "max_speed": 32,
            "released_copies": "13 000 copies",
            "description": "Запас хода этой машины  — 129 км. Доработанная версия Detroit Electric установила мировой рекорд дальности поездки на одной зарядке —  388 км.",
        },
        headers=admin_token,
    )

    assert res.status_code == 200

    res = client.post(
        "/",
        json={
            "brend": "Lincoln",
            "model": "Model L",
            "year": 1921,
            "engine": "combustion",
            # "max_speed": None,
            "released_copies": "2957 copies",
            "description": "Несмотря на колесную базу длиной 3,3м и V8 мощностью 81 л.с., из-за отсталого дизайна покупали машину неохотно.",
        },
        headers=admin_token,
    )

    assert res.status_code == 200

    res = client.post(
        "/",
        json={
            "brend": "Doble Steam Car",
            "model": "Doble Steam Car",
            "year": 1922,
            "engine": "steam",
            "max_speed": 190,
            "released_copies": "36 copies",
            "description": "Паровой автомобиль Doble Series E модели 1924 года мог проехать 2400 км, прежде чем его 24-галлонный резервуар для воды нужно было наполнить; даже в морозную погоду его можно было запустить из холода и тронуться с места в течение 30 секунд",
        },
        headers=admin_token,
    )

    assert res.status_code == 200


def test_get_all_data_cars(client, user_token):
    res = client.get("/", headers=user_token)
    assert "year" in res.get_json()[0]


def test_get_data_car(client, user_token):
    res = client.get("/Model L/", headers=user_token)
    assert res.status_code == 200
    assert "year" in res.get_json()


def test_send_data_user(client, user_token):
    res = client.post(
        "/",
        json={
            "brend": "test",
            "model": "test",
            "year": 3033,
            "engine": "test",
            "max_speed": 0,
            "released_copies": "test",
            "description": "test",
        },
        headers=user_token,
    )
    assert "No access" in res.get_json()["message"]


def test_make_update(client, admin_token):
    res = client.put(
        "/Model L/",
        json={
            "brend": "Lincoln",
            "max_speed": 120,
        },
        headers=admin_token,
    )

    assert res.status_code == 200
    assert res.get_json()["max_speed"] == 120


def test_admin_data_delete(client, admin_token):
    res = client.delete(
        "/Model L/",
        json={
            "brend": "Lincoln",
        },
        headers=admin_token,
    )

    assert "Entry deleted" in res.get_json()["message"]


def test_user_data_delete(client, user_token):
    res = client.delete(
        "/Model T/",
        json={
            "brend": "Ford",
        },
        headers=user_token,
    )

    assert "No access" in res.get_json()["message"]


def test_no_modele_data_delete(client, admin_token):
    res = client.delete(
        "/test-model/",
        json={
            "brend": "test",
        },
        headers=admin_token,
    )

    assert "No such model" in res.get_json()["message"]

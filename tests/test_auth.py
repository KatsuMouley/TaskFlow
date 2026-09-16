def test_register(client):
    response = client.post(
        "/auth/register",
        data={
            "name": "Carla",
            "email": "carla@example.com",
            "password": "abcdef",
            "confirm_password": "abcdef",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Conta criada" in response.text


def test_reject_duplicate_email(client):
    response = client.post(
        "/auth/register",
        data={
            "name": "Outra Ana",
            "email": "ANA@example.com",
            "password": "abcdef",
            "confirm_password": "abcdef",
        },
    )
    assert "já está cadastrado" in response.text


def test_login_and_logout(client, login):
    response = login()
    assert "Bem-vindo, Ana" in response.text
    response = client.post("/auth/logout", follow_redirects=True)
    assert "Você saiu" in response.text


def test_invalid_login(client, login):
    response = login(password="senha-errada")
    assert "inválidos" in response.text

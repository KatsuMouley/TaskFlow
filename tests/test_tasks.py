from app.extensions import db
from app.models import Task, User


def create_task(client, **overrides):
    data = {
        "title": "Preparar apresentação",
        "description": "Montar os slides finais",
        "status": "pending",
        "assigned_to_id": 1,
    }
    data.update(overrides)
    return client.post("/tasks/new", data=data, follow_redirects=True)


def test_dashboard_requires_login(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/auth/login" in response.location


def test_create_and_filter_task(client, login):
    login()
    response = create_task(client)
    assert "Tarefa criada" in response.text
    assert "Preparar apresentação" in response.text

    response = client.get("/tasks?status=completed")
    assert "Preparar apresentação" not in response.text
    response = client.get("/tasks?status=pending")
    assert "Preparar apresentação" in response.text


def test_assignee_can_edit_task(client, login, app):
    login()
    create_task(client, assigned_to_id=2)
    client.post("/auth/logout")
    login("bruno@example.com")
    response = client.post(
        "/tasks/1/edit",
        data={
            "title": "Apresentação revisada",
            "description": "Pronta",
            "status": "completed",
            "assigned_to_id": 2,
        },
        follow_redirects=True,
    )
    assert "Tarefa atualizada" in response.text
    assert "Concluída" in response.text


def test_only_creator_can_delete(client, login, app):
    login()
    create_task(client, assigned_to_id=2)
    client.post("/auth/logout")
    login("bruno@example.com")
    assert client.post("/tasks/1/delete").status_code == 403

    with app.app_context():
        assert db.session.get(Task, 1) is not None


def test_creator_can_delete(client, login, app):
    login()
    create_task(client)
    response = client.post("/tasks/1/delete", follow_redirects=True)
    assert "Tarefa excluída" in response.text
    with app.app_context():
        assert Task.query.count() == 0

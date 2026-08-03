import json
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, engine, get_db
from app.models.models import User


client = TestClient(app)


def setup_module(module):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def teardown_module(module):
    Base.metadata.drop_all(bind=engine)


def test_register_and_create_task():
    # Register a user
    register_response = client.post(
        "/api/users/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "full_name": "Test User",
            "password": "strongpassword",
        },
    )
    assert register_response.status_code == 201
    registered_user = register_response.json()
    assert registered_user["username"] == "testuser"
    assert registered_user["email"] == "testuser@example.com"

    # Login and get token
    login_response = client.post(
        "/api/users/login",
        data={"username": "testuser", "password": "strongpassword"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    assert token

    # Create project for the task
    project_response = client.post(
        "/api/projects/",
        json={"name": "Test Project", "description": "Project for testing", "owner_id": registered_user["id"]},
    )
    assert project_response.status_code == 201
    project_data = project_response.json()

    # Create task with authentication
    task_response = client.post(
        "/api/tasks/",
        json={
            "title": "Test Task",
            "description": "A task created in integration test",
            "project_id": project_data["id"],
            "status": "todo",
            "priority": "high",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert task_response.status_code == 200
    task_data = task_response.json()
    assert task_data["title"] == "Test Task"
    assert task_data["project_id"] == project_data["id"]

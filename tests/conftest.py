import os
import pytest

os.environ["DB_NAME"] = "task_management_test"

from fastapi.testclient import TestClient
from app.main import app
from app.database import get_connection


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def clean_database():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                TRUNCATE TABLE tasks, projects, users
                RESTART IDENTITY CASCADE;
                """
            )

    yield


@pytest.fixture
def auth_headers(client):
    client.post(
        "/users/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/users/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture
def project(client, auth_headers):
    response = client.post(
        "/projects",
        json={
            "name": "Test Project",
            "description": "Test Description"
        },
        headers=auth_headers
    )

    return response.json()


@pytest.fixture
def task(client, auth_headers, project):
    project_id = project["id"]

    response = client.post(
        f"/projects/{project_id}/tasks",
        json={
            "title": "Test Task",
            "description": "Test Task Description"
        },
        headers=auth_headers
    )

    return response.json()
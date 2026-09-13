def test_create_project(client, auth_headers):
    response = client.post(
        "/projects",
        json={
            "name": "Test Project",
            "description": "My first test project"
        },
        headers=auth_headers
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Project"
    assert data["description"] == "My first test project"

def test_get_projects(client, auth_headers):
    client.post(
        "/projects",
        json={
            "name": "Test Project",
            "description": "My first test project"
        },
        headers=auth_headers
    )
    response=client.get(
        "/projects",
        headers=auth_headers
    )

    assert response.status_code==200
    data = response.json()
    assert data[0]["name"] == "Test Project"
    assert data[0]["description"] == "My first test project"
def test_get_project(client, auth_headers):
    create_response=client.post(
            "/projects",
            json={
                "name": "Test Project",
                "description": "My first test project"
            },
            headers=auth_headers
        )
    project_id = create_response.json()["id"]
    response=client.get(
            f"/projects/{project_id}",
            headers=auth_headers
        )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"

def test_update_project(client, auth_headers):
    create_response=client.post(
                "/projects",
                json={
                    "name": "Test Project",
                    "description": "My first test project"
                },
                headers=auth_headers
            )
    project_id = create_response.json()["id"]
    response=client.patch(
        f"/projects/{project_id}",
        json={
            "name": "Updated Project"
            },

        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"]=="Updated Project"

def test_delete_project(client, auth_headers):
    create_response=client.post(
                    "/projects",
                    json={
                        "name": "Test Project",
                        "description": "My first test project"
                    },
                    headers=auth_headers
                )
    project_id = create_response.json()["id"]
    response=client.delete(
        f"/projects/{project_id}",
            headers=auth_headers

    )
    assert response.status_code == 200
    get_response = client.get(
    f"/projects/{project_id}",
    headers=auth_headers
    )

    assert get_response.status_code == 404


def test_user_cannot_access_another_users_project(client, auth_headers):


    create_response = client.post(
    "/projects",
    json={
        "name": "Private Project",
        "description": "User one project"
    },
    headers=auth_headers
    )

    project_id = create_response.json()["id"]

    response_user = client.post(
        "/users/register",
        json={
            "name": "Test User",
            "email": "test2@example.com",
            "password": "password123"
        }
    )

    assert response_user.status_code == 201

    data = response_user.json()

    assert data["name"] == "Test User"
    assert data["email"] == "test2@example.com"
    assert "password" not in data
    assert "password_hash" not in data

    response_login = client.post(
        "/users/login",
        json={
            "email": "test2@example.com",
            "password": "password123"
        }
    )

    assert response_login.status_code == 200

    data = response_login.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

    token = data["access_token"]

    second_user_headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get(
        f"/projects/{project_id}",
        headers=second_user_headers
    )

    assert response.status_code == 404







        

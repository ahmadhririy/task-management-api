def test_register_user(client):
    response = client.post(
        "/users/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert "password" not in data
    assert "password_hash" not in data


def test_login_user(client):
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

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client):
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
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 400

def test_register_duplicate_email(client):
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    }

    client.post(
        "/users/register",
        json=user_data
    )

    response = client.post(
        "/users/register",
        json=user_data
    )

    assert response.status_code == 400

def test_get_current_user(client):
    client.post(
        "/users/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/users/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"

def test_get_current_user_invalid_token(client):
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer invalid-token"
        }
    )

    assert response.status_code == 401


def test_update_user(client, auth_headers):
    response = client.patch(
        "/users/me",
        json={
            "name": "Updated User",
            "email": "updated@example.com"
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated User"
    assert data["email"] == "updated@example.com"

def test_update_password(client, auth_headers):
    response = client.patch(
        "/users/me/password",
        json={
            "current_password": "password123",
            "new_password": "newpassword123"
        },
        headers=auth_headers
    )

    assert response.status_code == 200

    response_pass = client.post(
        "/users/login",
        json= {
               "email": "test@example.com",
               "password": "newpassword123"
              }
    )
    assert response_pass.status_code == 200


def test_delete_user(client, auth_headers):
    response = client.delete(
        "/users/me",
        headers=auth_headers
    )

    assert response.status_code == 200

    response_get = client.get(
        "/users/me",
        headers=auth_headers
    )
    assert response_get.status_code == 401
    


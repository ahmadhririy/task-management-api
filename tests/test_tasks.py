def test_create_task(client, auth_headers):
    create_response=client.post(
        "/projects",
        json={
            "name": "Test Project",
            "description": "My first test project"
        },
        headers=auth_headers
    )
    project_id=create_response.json()["id"]

    response=client.post(
        f"/projects/{project_id}/tasks",
        json={
            "title":"test task",
            "description":"My first test task"
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    data=response.json()
    assert data["title"]=="test task"
    assert data["status"]=="todo"
    assert data["project_id"]==project_id

def test_get_tasks(client, auth_headers):
    create_project=client.post("/projects",
        json={
                 "name":"test project",
                 "description": "My first test task"                  
            },
            headers=auth_headers
    )
    project_id=create_project.json()["id"]
    create_task=client.post(
        f"/projects/{project_id}/tasks",
        json={
            "title":"test task",
            "description":"My first test task"
        },
        headers=auth_headers
    )
    assert create_task.status_code == 201
    response = client.get(
    f"/projects/{project_id}/tasks",
    headers=auth_headers
)

    assert response.status_code == 200

    data = response.json()
    assert data[0]["title"]=="test task"

def test_get_task(client, auth_headers):
    create_project=client.post(
            "/projects",
            json={
                "name": "Test Project",
                "description": "My first test project"
            },
            headers=auth_headers
    )
    project_id=create_project.json()["id"]
    create_task=client.post(
            f"/projects/{project_id}/tasks",
            json={
                "title":"test task",
                "description":"My first test task"
            },
            headers=auth_headers
        )
    task_id=create_task.json()["id"]
    response=client.get(
        f"/projects/{project_id}/tasks/{task_id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "test task"
    assert data["id"] == task_id
    assert data["project_id"] == project_id

def test_update_task(client, auth_headers):
    create_project=client.post(
        "/projects",
        json={
             "name": "Test Project",
              "description": "My first test project"
            },
            headers=auth_headers
        )
    project_id=create_project.json()["id"]
    create_task=client.post(
        f"/projects/{project_id}/tasks",
            json={
             "title":"test task",
             "description":"My first test task"
            },
                headers=auth_headers
            )
    task_id=create_task.json()["id"]
    response=client.patch(f"/projects/{project_id}/tasks/{task_id}",
        json={
             "status":"in_progress"
             },
             headers=auth_headers
             )
    assert response.status_code == 200
    data=response.json()
    assert data["status"]=="in_progress"

def test_delete_task(client, auth_headers):
    create_project=client.post(
                "/projects",
                json={
                    "name": "Test Project",
                    "description": "My first test project"
                },
                headers=auth_headers
        )
    project_id=create_project.json()["id"]
    create_task=client.post(
        f"/projects/{project_id}/tasks",
             json={
                    "title":"test task",
                    "description":"My first test task"
                },
                headers=auth_headers
            )
    task_id=create_task.json()["id"]
    response = client.delete(
    f"/projects/{project_id}/tasks/{task_id}",
    headers=auth_headers
    )
    assert response.status_code==200
    get_response = client.get(
    f"/projects/{project_id}/tasks/{task_id}",
    headers=auth_headers
    )
    assert get_response.status_code==404

def test_user_cannot_access_another_users_task(client, project, task):
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
    project_id = project["id"]
    task_id = task["id"]
    response = client.get(
    f"/projects/{project_id}/tasks/{task_id}",
    headers=second_user_headers
    )

    assert response.status_code == 404




    



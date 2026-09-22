# Task Management API

A full-stack Task Management application built with **FastAPI**, **PostgreSQL**, and vanilla **HTML/CSS/JavaScript**.

The application allows users to create an account, manage projects and tasks, update their profile, and securely access only their own data using JWT authentication.

---

## Features

### Authentication
- User registration
- User login
- JWT authentication
- Password hashing
- Protected endpoints
- User-specific data access

### User Profile
- View profile
- Update name and email
- Change password
- Delete account
- Automatic deletion of the user's projects and tasks

### Projects
- Create projects
- View projects
- Update projects
- Delete projects
- Each user can only access their own projects

### Tasks
- Create tasks inside projects
- View project tasks
- Update tasks
- Delete tasks
- Task status support:
  - `todo`
  - `in_progress`
  - `done`

### Frontend
- Login and registration pages
- Dashboard
- Project management
- Task management
- Profile management
- Dashboard statistics
- Custom toast notifications
- Custom confirmation modals
- Responsive interface

### Testing
- Authentication tests
- Project CRUD tests
- Task CRUD tests
- Profile tests
- Separate PostgreSQL test database

---

## Tech Stack

### Backend
- Python
- FastAPI
- Pydantic
- Psycopg
- PostgreSQL
- JWT
- pwdlib

### Frontend
- HTML
- CSS
- JavaScript

### Testing
- Pytest
- FastAPI TestClient

### DevOps
- Docker
- Docker Compose

---

## Project Structure

```text
Task_Management/
│
├── app/
│   ├── routers/
│   │   ├── projects.py
│   │   ├── tasks.py
│   │   └── users.py
│   │
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── schemas.py
│   └── security.py
│
├── tests/
│   ├── conftest.py
│   ├── test_users.py
│   ├── test_projects.py
│   └── test_tasks.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── .env
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## API Endpoints

### Users

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users/register` | Register a new user |
| POST | `/users/login` | Login and receive an access token |
| GET | `/users/me` | Get current user |
| PATCH | `/users/me` | Update profile |
| PATCH | `/users/me/password` | Change password |
| DELETE | `/users/me` | Delete account |

### Projects

| Method | Endpoint | Description |
|---|---|---|
| GET | `/projects` | Get user's projects |
| POST | `/projects` | Create a project |
| GET | `/projects/{project_id}` | Get a project |
| PATCH | `/projects/{project_id}` | Update a project |
| DELETE | `/projects/{project_id}` | Delete a project |

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| GET | `/projects/{project_id}/tasks` | Get project tasks |
| POST | `/projects/{project_id}/tasks` | Create a task |
| GET | `/projects/{project_id}/tasks/{task_id}` | Get a task |
| PATCH | `/projects/{project_id}/tasks/{task_id}` | Update a task |
| DELETE | `/projects/{project_id}/tasks/{task_id}` | Delete a task |

---

## Security

The application implements:

- Password hashing
- JWT-based authentication
- Protected API endpoints
- Project ownership validation
- Task ownership through project ownership
- Environment variables for sensitive configuration
- PostgreSQL constraints
- Cascade deletion for related data

Users cannot access or modify projects and tasks owned by another user.

---

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/ahmadhririy/task-management-api.git
cd task-management-api
```

### 2. Configure environment variables

Create a `.env` file in the project root.

Example:

```env
DB_NAME=task_management
DB_USER=postgres
DB_PASSWORD=your_database_password
DB_HOST=db
DB_PORT=5432
SECRET_KEY=your_secret_key
```

Do not commit the `.env` file to GitHub.

### 3. Start the backend

```bash
docker compose up -d --build
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### 4. Start the frontend

From the project directory:

```bash
python -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500/frontend/
```

---

## Running Tests

Run the test suite inside the API container:

```bash
docker compose exec api python -m pytest -v
```

The tests use a separate PostgreSQL database named:

```text
task_management_test
```

---

## Database Relationships

```text
User
  |
  | 1
  |
  | many
  v
Projects
  |
  | 1
  |
  | many
  v
Tasks
```

Deleting a user automatically deletes their projects and tasks.

Deleting a project automatically deletes its tasks.

---

## Task Status

A task can have one of the following statuses:

```text
todo
in_progress
done
```

The allowed values are validated by both the API and the database.

---

## Author

**Ahmad Alhriri**

Computer Science Student  
Backend Developer
# Task Management API

A RESTful Task Management API built with FastAPI and PostgreSQL.

The application allows users to register, log in, create their own projects, and manage tasks inside those projects. Authentication is handled using JWT, and users can only access projects and tasks that belong to them.

## Features

- User registration
- User login with JWT authentication
- Password hashing
- Protected endpoints
- Create, read, update, and delete projects
- Create, read, update, and delete tasks
- Project ownership authorization
- Task status management
- PostgreSQL database
- Database-level task status validation
- Automated API tests with Pytest
- Docker and Docker Compose support

## Technologies

- Python
- FastAPI
- PostgreSQL
- Psycopg
- Pydantic
- JWT
- pwdlib
- Pytest
- Docker
- Docker Compose

## Project Structure

```text
Task_Management/
├── app/
│   ├── routers/
│   │   ├── projects.py
│   │   ├── tasks.py
│   │   └── users.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── schemas.py
│   └── security.py
├── tests/
│   ├── conftest.py
│   ├── test_users.py
│   ├── test_projects.py
│   └── test_tasks.py
├── .dockerignore
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Database Structure

The application uses three main tables:

### Users

```text
users
├── id
├── name
├── email
└── password_hash
```

### Projects

```text
projects
├── id
├── name
├── description
└── user_id
```

Each project belongs to one user.

### Tasks

```text
tasks
├── id
├── title
├── description
├── status
└── project_id
```

Each task belongs to one project.

Task status can only be:

```text
todo
in_progress
done
```

## API Endpoints

### Users

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users/register` | Register a new user |
| POST | `/users/login` | Login and receive JWT |
| GET | `/users/me` | Get the authenticated user |

### Projects

| Method | Endpoint | Description |
|---|---|---|
| POST | `/projects` | Create a project |
| GET | `/projects` | Get user's projects |
| GET | `/projects/{project_id}` | Get a project |
| PATCH | `/projects/{project_id}` | Update a project |
| DELETE | `/projects/{project_id}` | Delete a project |

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| POST | `/projects/{project_id}/tasks` | Create a task |
| GET | `/projects/{project_id}/tasks` | Get project tasks |
| GET | `/projects/{project_id}/tasks/{task_id}` | Get a task |
| PATCH | `/projects/{project_id}/tasks/{task_id}` | Update a task |
| DELETE | `/projects/{project_id}/tasks/{task_id}` | Delete a task |

## Authentication

Protected endpoints require a JWT Bearer token.

After logging in, include the token in the request header:

```text
Authorization: Bearer <your_token>
```

Users can only access their own projects and the tasks inside those projects.

## Environment Variables

Create a `.env` file in the project root:

```env
DB_NAME=task_management
DB_USER=postgres
DB_PASSWORD=your_database_password
DB_HOST=db
DB_PORT=5432
SECRET_KEY=your_secret_key
```

Do not commit the `.env` file to GitHub.

## Running with Docker

Build and start the application:

```bash
docker compose up -d --build
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

To stop the application:

```bash
docker compose down
```

## Running Tests

The project includes automated tests for users, authentication, projects, tasks, and ownership authorization.

Run the tests inside the API container:

```bash
docker compose exec api python -m pytest -v
```

## Security

- Passwords are hashed before being stored.
- JWT tokens are used for authentication.
- Protected endpoints require authentication.
- Users cannot access projects owned by other users.
- Users cannot access tasks through projects they do not own.
- Task status is validated by both the API and PostgreSQL.

## Future Improvements

Possible future improvements include:

- Database migrations with Alembic
- Connection pooling
- Refresh tokens
- Project pagination
- Task filtering and pagination
- Task due dates and priorities
- CI/CD with GitHub Actions
- Deployment to a cloud platform

## Author

Ahmad
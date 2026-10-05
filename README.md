# Task Management API

A full-stack Task Management application built with **FastAPI**, **PostgreSQL**, and vanilla **HTML/CSS/JavaScript**.

The application allows users to create an account, manage projects and tasks, update their profile, and securely access only their own data using JWT authentication.

The project also includes database migrations, pagination, filtering, search, centralized configuration, logging, automated testing, and Docker support.

---

## Features

### Authentication

- User registration
- User login
- JWT authentication
- Password hashing
- Protected endpoints
- User-specific data access
- Token expiration handling

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
- Pagination support

### Tasks

- Create tasks inside projects
- View project tasks
- Update tasks
- Delete tasks
- Each task is protected through project ownership
- Pagination support
- Filter tasks by status
- Search tasks by title
- Combine filtering, search, and pagination

Supported task statuses:

- `todo`
- `in_progress`
- `done`

Example:

```text
GET /projects/2/tasks?status=done&search=fastapi&page=1&limit=10
```

### Database

- PostgreSQL relational database
- Foreign key relationships
- Cascade deletion
- Database constraints
- Database indexes
- Alembic database migrations
- Migration upgrade and downgrade support
- Fresh database migration support

Indexes are used on important foreign key columns:

```text
projects.user_id
tasks.project_id
```

### Error Handling

- FastAPI HTTP exception handling
- Global exception handler for unexpected errors
- Safe `500 Internal Server Error` responses
- Internal exception details are not exposed to API clients

### Logging

- Application logging using Python's `logging` module
- INFO-level application logs
- Error logging for unexpected exceptions
- Exception traceback logging for debugging

### Configuration

- Environment-based configuration
- Centralized configuration in `app/config.py`
- Database credentials loaded from environment variables
- JWT secret loaded from environment variables
- Required configuration validation
- Application fails fast when required configuration is missing
- `.env` excluded from Git and Docker build context

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
- Automated testing with Pytest

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
- Alembic

### Frontend

- HTML
- CSS
- JavaScript

### Testing

- Pytest
- FastAPI TestClient
- Separate PostgreSQL test database

### DevOps

- Docker
- Docker Compose
- Environment variables
- Alembic migrations

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
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── schemas.py
│   └── security.py
│
├── alembic/
│   ├── versions/
│   │   ├── 7d09af13797f_initial_schema.py
│   │   ├── 5605f9b235d9_add_created_at_to_users.py
│   │   ├── ee85f058f315_add_phone_to_users.py
│   │   └── c237a70c04e3_add_foreign_key_indexes.py
│   │
│   ├── env.py
│   ├── README
│   └── script.py.mako
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
├── alembic.ini
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
| GET | `/projects` | Get user's projects with pagination |
| POST | `/projects` | Create a project |
| GET | `/projects/{project_id}` | Get a project |
| PATCH | `/projects/{project_id}` | Update a project |
| DELETE | `/projects/{project_id}` | Delete a project |

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| GET | `/projects/{project_id}/tasks` | Get tasks with pagination, filtering, and search |
| POST | `/projects/{project_id}/tasks` | Create a task |
| GET | `/projects/{project_id}/tasks/{task_id}` | Get a task |
| PATCH | `/projects/{project_id}/tasks/{task_id}` | Update a task |
| DELETE | `/projects/{project_id}/tasks/{task_id}` | Delete a task |

---

## Pagination

Projects and tasks support pagination using the following query parameters:

```text
page
limit
```

Example:

```text
GET /projects?page=1&limit=10
```

The API calculates the SQL offset using:

```text
offset = (page - 1) * limit
```

The maximum allowed `limit` is `100`.

Task pagination can also be combined with filtering and search.

---

## Task Filtering

Tasks can be filtered by status using:

```text
status
```

Example:

```text
GET /projects/2/tasks?status=done
```

Supported values:

```text
todo
in_progress
done
```

---

## Task Search

Tasks can be searched by title using the `search` query parameter.

Example:

```text
GET /projects/2/tasks?search=fastapi
```

Search is case-insensitive using PostgreSQL `ILIKE`.

Filtering, searching, and pagination can be combined:

```text
GET /projects/2/tasks?status=done&search=fastapi&page=1&limit=10
```

---

## Security

The application implements:

- Password hashing
- JWT-based authentication
- Token expiration
- Protected API endpoints
- Project ownership validation
- Task ownership through project ownership
- Parameterized SQL queries
- Environment variables for sensitive configuration
- Centralized application configuration
- PostgreSQL constraints
- Foreign key constraints
- Cascade deletion for related data

Users cannot access or modify projects and tasks owned by another user.

Sensitive values such as database passwords and the JWT secret are stored in environment variables and are not committed to Git.

---

## Error Handling

Expected API errors are handled using FastAPI HTTP exceptions.

Examples include:

```text
400 Bad Request
401 Unauthorized
404 Not Found
422 Unprocessable Entity
```

Unexpected application errors are handled by a global exception handler.

Clients receive a safe response:

```json
{
  "detail": "Internal server error"
}
```

The actual exception and traceback are logged on the server instead of being exposed to the client.

---

## Logging

The application uses Python's built-in logging system.

Example log format:

```text
timestamp - level - logger - message
```

Unexpected exceptions are logged with their traceback to help with debugging while keeping internal error details hidden from API users.

---

## Configuration

Application configuration is centralized in:

```text
app/config.py
```

Configuration values are loaded from environment variables.

Required settings include:

```text
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
SECRET_KEY
```

The application validates required configuration during startup.

If a required setting is missing, the application fails immediately instead of running with invalid configuration.

---

## Database Migrations

Database schema changes are managed using **Alembic**.

The migration history includes:

```text
Initial database schema
↓
Add created_at to users
↓
Add phone to users
↓
Add foreign key indexes
```

### Apply All Migrations

```bash
docker compose exec api alembic upgrade head
```

### Check Current Migration

```bash
docker compose exec api alembic current
```

### View Migration History

```bash
docker compose exec api alembic history
```

### Upgrade One Migration

```bash
docker compose exec api alembic upgrade +1
```

### Downgrade One Migration

```bash
docker compose exec api alembic downgrade -1
```

Alembic allows the database schema to evolve in a controlled and reproducible way.

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

Relationship keys:

```text
projects.user_id → users.id
tasks.project_id → projects.id
```

Deleting a user automatically deletes their projects and tasks.

Deleting a project automatically deletes its tasks.

---

## Database Constraints

Task status is restricted at the database level.

Allowed values:

```text
todo
in_progress
done
```

This validation exists both in the API and in PostgreSQL.

The database also uses:

- Primary keys
- Foreign keys
- Unique email constraint
- NOT NULL constraints
- CHECK constraint for task status
- Cascade deletion

---

## Database Indexes

Indexes are created for commonly used foreign key lookups:

```text
idx_projects_user_id
idx_tasks_project_id
```

These improve queries such as retrieving projects belonging to a user and tasks belonging to a project.

The indexes are managed through Alembic migrations.

---

## Running the Project

### 1. Clone the Repository

```bash
git clone https://github.com/ahmadhririy/task-management-api.git
cd task-management-api
```

### 2. Configure Environment Variables

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

### 3. Build and Start the Containers

```bash
docker compose up -d --build
```

Check container status:

```bash
docker compose ps
```

### 4. Apply Database Migrations

```bash
docker compose exec api alembic upgrade head
```

### 5. Open the API

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the Frontend

From the project directory:

```bash
python -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500/frontend/
```

### 7. Stop the Application

```bash
docker compose down
```

---

## Running Tests

Run the complete test suite inside the API container:

```bash
docker compose exec api python -m pytest -v
```

The tests use a separate PostgreSQL database:

```text
task_management_test
```

This keeps test data separate from the main application database.

---

## Task Status

A task can have one of the following statuses:

```text
todo
in_progress
done
```

The allowed values are validated by both the API and the PostgreSQL database.

---

## Author

**Ahmad Alhriri**

Computer Science Student  
Backend Developer
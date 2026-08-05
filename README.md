# TaskHub API

A Task Management REST API built with **FastAPI**, following a layered architecture with JWT authentication, Workspace RBAC, Redis caching, and MySQL.

## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy 2.x (Async)
- Alembic
- MySQL 8
- Redis 7
- Pydantic v2
- JWT Authentication
- Docker & Docker Compose
- Ruff
- mypy

---

## Features

### Authentication

- Register
- Login
- Refresh Token
- Logout

### Users

- Get current profile
- Update profile
- Change password

### Workspaces

- CRUD workspace
- Invite member
- Remove member
- Workspace RBAC (OWNER / EDITOR / VIEWER)

### Projects

- CRUD project
- Archive project
- Workspace permission check

### Tasks

- CRUD task
- Assign task
- Status
- Priority
- Due date
- Filtering
- Pagination
- Redis cache

### Labels

- CRUD label
- Assign label to task
- Remove label from task

### Comments

- CRUD comment
- Author permission
- Workspace RBAC

### Documentation

- Swagger UI
- ReDoc
- Bearer Authentication
- Standard API error responses

---

## Project Structure

```text
taskhub-api/
│
├── app/
│   ├── api/
│   ├── background/
│   ├── core/
│   ├── db/
│   ├── dependencies/
│   ├── exceptions/
│   ├── middlewares/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── alembic/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/Duhydi/taskhub-api.git
cd taskhub-api
```

Create virtual environment

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies

```bash
pip install -r requirements.txt
```

Development tools

```bash
pip install -r requirements-dev.txt
```

Run migration

```bash
alembic upgrade head
```

Run application

```bash
uvicorn app.main:app --reload
```

---

## Docker

Start services

```bash
docker compose up --build
```

Stop services

```bash
docker compose down
```

---

## API Documentation

Swagger

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## API Endpoints

### Authentication

```
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
```

### Users

```
GET   /api/v1/users/me
PATCH /api/v1/users/me
PATCH /api/v1/users/change-password
```

### Workspaces

```
GET    /api/v1/workspaces
POST   /api/v1/workspaces
GET    /api/v1/workspaces/{workspace_id}
PATCH  /api/v1/workspaces/{workspace_id}
DELETE /api/v1/workspaces/{workspace_id}
```

### Workspace Members

```
POST   /api/v1/workspaces/{workspace_id}/members
GET    /api/v1/workspaces/{workspace_id}/members
DELETE /api/v1/workspaces/{workspace_id}/members/{user_id}
```

### Projects

```
POST   /api/v1/workspaces/{workspace_id}/projects
GET    /api/v1/workspaces/{workspace_id}/projects
GET    /api/v1/projects/{project_id}
PATCH  /api/v1/projects/{project_id}
PATCH  /api/v1/projects/{project_id}/archive
DELETE /api/v1/projects/{project_id}
```

### Tasks

```
GET    /api/v1/projects/{project_id}/tasks
POST   /api/v1/projects/{project_id}/tasks
GET    /api/v1/tasks/{task_id}
PATCH  /api/v1/tasks/{task_id}
DELETE /api/v1/tasks/{task_id}
```

Supported filters

```
status
priority
assignee_id
page
limit
```

### Labels

```
POST   /api/v1/projects/{project_id}/labels
GET    /api/v1/projects/{project_id}/labels
PATCH  /api/v1/labels/{label_id}
DELETE /api/v1/labels/{label_id}

POST   /api/v1/tasks/{task_id}/labels/{label_id}
DELETE /api/v1/tasks/{task_id}/labels/{label_id}
```

### Comments

```
POST   /api/v1/tasks/{task_id}/comments
GET    /api/v1/tasks/{task_id}/comments
PATCH  /api/v1/comments/{comment_id}
DELETE /api/v1/comments/{comment_id}
```

---

## RBAC

### System Roles

- ADMIN
- MEMBER

### Workspace Roles

- OWNER
- EDITOR
- VIEWER

| Feature         | OWNER | EDITOR | VIEWER | ADMIN |
| --------------- | :---: | :----: | :----: | :---: |
| View Workspace  |  ✓   |   ✓   |   ✓   |  ✓   |
| Manage Projects |  ✓   |   ✓   |   X   |  ✓   |
| Archive Project |  ✓   |   X   |   X   |  ✓   |
| Manage Tasks    |  ✓   |   ✓   |   X   |  ✓   |
| Manage Labels   |  ✓   |   ✓   |   X   |  ✓   |
| View Comments   |  ✓   |   ✓   |   ✓   |  ✓   |

---

## Code Quality

Run Ruff

```bash
ruff check app
```

Run mypy

```bash
mypy app
```

Current status

- Ruff: All checks passed
- mypy: Success (0 errors)

---

## Repository

GitHub

https://github.com/Duhydi/taskhub-api

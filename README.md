# Blogging Platform API

A RESTful API for a personal blogging platform built with FastAPI and SQLite. This project was built to learn FastAPI, REST API design, and basic full stack development concepts.

## What I Learned

- How to build a RESTful API with FastAPI
- HTTP methods: `GET`, `POST`, `PATCH`, `DELETE`
- HTTP status codes: `200`, `201`, `204`, `404`, `422`
- How to connect to a database using SQLAlchemy
- How to validate request/response data using Pydantic schemas
- Path parameters vs query parameters
- Dependency injection with `Depends()`
- Auto-generated API documentation with Swagger UI

## Project Structure

```
Blogging-Platform-API/
├── main.py          # FastAPI app entry point, registers routes
├── database.py      # Database connection and session setup
├── models.py        # Database table definitions (SQLAlchemy)
├── schemas.py       # Request/response shapes (Pydantic)
├── crud.py          # Database operations (Create, Read, Update, Delete)
├── routers/
│   └── posts.py     # All /posts API routes
└── requirements.txt
```

## Tech Stack

- **FastAPI** — web framework
- **SQLite** — database (stored in `blog.db`)
- **SQLAlchemy** — ORM for database operations
- **Pydantic** — data validation
- **Uvicorn** — ASGI server

## Setup

1. Install dependencies:
```
python3 -m pip install fastapi uvicorn sqlalchemy
```

2. Run the server:
```
python3 -m uvicorn main:app --reload
```

3. Open the interactive docs at `http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/posts/` | Create a new blog post |
| `GET` | `/posts/` | Get all blog posts |
| `GET` | `/posts/?search=term` | Filter posts by search term |
| `GET` | `/posts/{id}` | Get a single post by ID |
| `PATCH` | `/posts/{id}` | Update a post (partial update) |
| `DELETE` | `/posts/{id}` | Delete a post |

## Example Request

**Create a post:**
```json
POST /posts/
{
  "title": "My First Post",
  "content": "Hello from my blogging API!",
  "category": "Tech",
  "tags": "fastapi, python"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "My First Post",
  "content": "Hello from my blogging API!",
  "category": "Tech",
  "tags": "fastapi, python",
  "created_at": "2026-03-17T00:56:26",
  "updated_at": null
}
```

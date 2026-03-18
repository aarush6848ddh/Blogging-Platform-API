# Blogging Platform API

A RESTful API for a personal blogging platform built with FastAPI, PostgreSQL, and Redis. Built to learn FastAPI, containerization with Docker, and caching patterns.

## Architecture

```
                        ┌─────────────────────────────────────┐
                        │         Docker Network              │
                        │                                     │
  HTTP Request          │  ┌─────────────┐                   │
──────────────────────► │  │   FastAPI   │                   │
  localhost:8000        │  │  (Uvicorn)  │                   │
                        │  └──────┬──────┘                   │
                        │         │                           │
                        │    GET /posts/{id}?                 │
                        │         │                           │
                        │   ┌─────▼──────┐   cache hit       │
                        │   │   Redis    │ ──────────────►    │
                        │   │  (port 6379)│   return JSON     │
                        │   └─────┬──────┘                   │
                        │         │ cache miss                │
                        │   ┌─────▼──────┐                   │
                        │   │ PostgreSQL │                    │
                        │   │ (port 5432)│                    │
                        │   └────────────┘                    │
                        │                                     │
                        └─────────────────────────────────────┘
```

**Request flow for `GET /posts/{id}`:**
1. FastAPI checks Redis for `post:{id}`
2. Cache hit → return instantly (no DB query)
3. Cache miss → query PostgreSQL, store result in Redis for 60s, return post

All other endpoints go directly to PostgreSQL.

## What I Learned

- How to build a RESTful API with FastAPI
- HTTP methods: `GET`, `POST`, `PATCH`, `DELETE`
- HTTP status codes: `200`, `201`, `204`, `404`, `422`
- How to connect to a database using SQLAlchemy
- How to validate request/response data using Pydantic schemas
- Path parameters vs query parameters
- Dependency injection with `Depends()`
- Auto-generated API docs with Swagger UI
- Swapping SQLite for PostgreSQL
- Containerizing an app with Docker and docker-compose
- Wiring multiple services together in a Docker network
- Fixing container startup race conditions with healthchecks
- Caching with Redis (`get`, `setex`, cache-aside pattern)

## Project Structure

```
Blogging-Platform-API/
├── main.py              # FastAPI app entry point, registers routes
├── database.py          # Database connection and session setup
├── models.py            # Database table definitions (SQLAlchemy)
├── schemas.py           # Request/response shapes (Pydantic)
├── crud.py              # Database operations (Create, Read, Update, Delete)
├── routers/
│   └── posts.py         # All /posts API routes + Redis caching
├── Dockerfile           # Container definition for the FastAPI app
├── docker-compose.yml   # Orchestrates FastAPI + PostgreSQL + Redis
└── requirements.txt
```

## Tech Stack

| Tool | Purpose |
|------|---------|
| **FastAPI** | Web framework |
| **PostgreSQL** | Primary database |
| **Redis** | In-memory cache |
| **SQLAlchemy** | ORM for database operations |
| **Pydantic** | Data validation |
| **Uvicorn** | ASGI server |
| **Docker** | Containerization |
| **docker-compose** | Multi-container orchestration |

## Running with Docker

```bash
docker compose up --build
```

All three services (FastAPI, PostgreSQL, Redis) start automatically. FastAPI waits for PostgreSQL to be healthy before starting.

Open the interactive docs at `http://localhost:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/posts/` | Create a new blog post |
| `GET` | `/posts/` | Get all blog posts |
| `GET` | `/posts/?search=term` | Filter posts by title |
| `GET` | `/posts/{id}` | Get a single post by ID (Redis cached) |
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
  "created_at": "2026-03-18T00:07:39.304489Z",
  "updated_at": null
}
```
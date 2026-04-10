# Pastebin Clone

A REST API for storing and retrieving text snippets with a TTL. Built as a system design study project.

## Stack

- **FastAPI** — HTTP API
- **PostgreSQL** — persistent storage
- **Redis** — TTL-aware cache
- **SQLModel** — ORM + validation

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/pastes/` | Create a paste |
| `GET` | `/pastes/{code}` | Retrieve a paste |

### POST /pastes/

```json
{
  "input": "print('hello world')",
  "language": "python",
  "ttl": 3600
}
```

Returns the created paste with a short `code` and `expiration_time`.

### GET /pastes/{code}

Returns the paste if still valid. Returns `410 Gone` if expired.

## Setup

**Prerequisites:** Python 3.11+, PostgreSQL, Redis

```bash
pip install -r requirements.txt
```

```bash
fastapi dev app/main.py
```

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

# Notes API

A simple REST API for managing personal notes, built with FastAPI. Created to practice authentication, database design, and clean API architecture.

## Features
- User registration
- User authentication with JWT
- Create notes
- Get all notes of the authenticated user
- Update notes
- Delete notes
- Password hashing
- SQLite database
- SQLAlchemy ORM
- Alembic migrations

## Technologies
- Python 3.12+
- FastAPI
- SQLAlchemy
- Alembic
- SQLite
- AuthX (JWT Authentication)
- Pydantic
- pwdlib

## API Endpoints

| Method | Endpoint | Description | Success |
|--------|----------|-------------|---------|
| POST | `/signup` | Register a new user | `200` |
| POST | `/login` | Log in and receive an access + refresh token pair | `200` |
| POST | `/refresh` | Exchange a refresh token for a new access token | `200` |
| GET | `/notes` | Get all of the authenticated user's notes | `200` |
| POST | `/notes` | Create a note | `200` |
| PUT | `/notes/{note_id}` | Update a note, returns the updated note | `200` |
| DELETE | `/notes/{note_id}` | Delete a note, empty body | `204` |
| GET | `/health` | Liveness check | `200` |

Responses are camelCase. All `/notes` endpoints require `Authorization: Bearer <access_token>`
and only ever see notes belonging to the token's owner.

### Example: create a note

Request:
```json
POST /notes
Authorization: Bearer <access_token>

{
  "title": "Shopping list",
  "content": "Milk, eggs, bread"
}
```

Response:
```json
{
  "id": 1,
  "title": "Shopping list",
  "content": "Milk, eggs, bread"
}
```

### Tokens

`/login` returns two tokens:

```json
{
  "accessToken": "<15 minutes>",
  "refreshToken": "<20 days>"
}
```

Send the **access** token to every endpoint. When it expires, `POST /refresh` with the
**refresh** token in the `Authorization` header to get a new access token — no password needed:

```json
POST /refresh
Authorization: Bearer <refresh_token>

{ "accessToken": "<new, 15 minutes>" }
```

The two are not interchangeable: an access token sent to `/refresh` is rejected, and a refresh
token sent to `/notes` is rejected. There is currently no logout — a JWT can't be revoked, so
the short access-token lifetime is what limits the damage from a leaked one.

## Configuration

Create a `.env` file in the project root:

JWT_SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./notes.db

## Running the project

```bash
git clone <https://github.com/Just-Forest/notes-api.git>
cd NotesAPI
uv sync
alembic upgrade head
uvicorn main:app --reload
```

Open Swagger UI:
http://127.0.0.1:8000/docs

## Tests

```bash
pytest -q
```

19 tests, at two levels: `tests/test_auth.py` and `tests/test_notes.py` go through the API with
`TestClient`, while `tests/test_services.py` calls the service classes directly with no HTTP.
`tests/conftest.py` overrides `get_session` onto a separate `test.db`, so the suite never touches
the development database.

## Future Improvements
- PostgreSQL + Docker
- `created_at` on notes, then pagination on `GET /notes`
- Search notes
- Refresh-token rotation and logout (needs a denylist table)

## License
MIT
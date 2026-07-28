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

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/signup` | Register a new user |
| POST | `/login` | Login and receive JWT token |
| GET | `/notes` | Get all user's notes |
| POST | `/notes` | Create a new note |
| PUT | `/notes/{note_id}` | Update a note |
| DELETE | `/notes/{note_id}` | Delete a note |

### Example: Create a note

Request:
```json
POST /notes
Authorization: Bearer <your_jwt_token>

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
  "content": "Milk, eggs, bread",
  "owner_id": 3
}
```

## Configuration

Create a `.env` file in the project root:

SECRET_KEY=your-secret-key
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

## Future Improvements
- Search notes
- Pagination
- Docker support
- PostgreSQL
- Unit tests

## License
MIT
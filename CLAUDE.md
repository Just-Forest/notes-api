# CLAUDE.md

Notes API — FastAPI + SQLAlchemy 2.0 + Alembic + SQLite. A learning project being refactored
from a working-but-tangled state toward clean layering. See [TASKS.md](TASKS.md) for the
roadmap and the reasoning behind each completed step.

## Working with this user

- **They are learning.** Explain the *concept* behind a fix, not just the fix.
- **Established rhythm: they implement, you review.** Offer to make edits; don't assume. When
  they've iterated twice on the same thing and it's still broken, finishing it is fine — say
  clearly what you changed.
- **Verify claims by running things.** Several "done" states in this project turned out to be
  broken (migrations that never ran, tests hitting the dev DB, undeclared dependencies).
  "The file exists" is not "it works."

## Environment

- **Windows.** The user runs commands in `cmd.exe`. POSIX commands (`rm`, `ls`, `&&` chains in
  PowerShell 5.1) fail for them. Use `del /q`, `dir`, one command per line.
- Python 3.12, `uv`-managed venv at `.venv`. Console scripts live in `.venv\Scripts\`.
- Dev database is `notes.db` (gitignored). `authors.db` is a dead name from an older
  authors/books project — if it reappears, something is bypassing config.

## Commands

```
pytest -q
alembic check
alembic upgrade head
ruff check .
uvicorn main:app --reload
```

**The verification triad is `ruff check .` + `pytest -q` + `alembic check`.** Run all three
after any structural change. `alembic check` must say "No new upgrade operations detected."

## Architecture

```
main.py                     app assembly + exception handlers only
src/
├── config.py               Settings (pydantic-settings) — single source for env config
├── security.py             AuthX/JWT setup
├── api/
│   ├── dependencies.py     get_current_user, get_note_service (shared providers)
│   ├── router.py           aggregates sub-routers; declares NO routes
│   ├── endpoints/          one module per resource: auth.py, notes.py, health.py
│   └── schemas/            Pydantic; all inherit BaseSchema (camelCase aliases)
├── database/
│   ├── session.py          engine, Base, session_factory, get_session
│   ├── user.py, note.py    ORM models
└── services/               business logic; exceptions.py holds domain errors
alembic/                    migrations (env.py owns the DB URL)
tests/                      conftest.py overrides get_session onto test.db
```

### Layering rules

| Layer | Owns | Must never contain |
|---|---|---|
| `endpoints/` | status codes, `Depends`, response models | SQL |
| `services/` | business rules, transactions | `HTTPException` |
| `database/` | schema, session plumbing | HTTP or business rules |

Dependencies point **downward only**. An endpoint module importing from `main` is always a
bug — it creates a cycle, and it means an object that should be local is missing.

## Invariants — do not break these

1. **`session_factory` must not be imported outside `src/database/session.py`.** Endpoints and
   services receive a `Session` via `Depends(get_session)`. This is the seam that lets
   `tests/conftest.py` redirect to `test.db` with `app.dependency_overrides[get_session]`.
   If anything reaches the global factory directly, tests silently hit the dev database.

2. **`alembic/env.py` must import `User` and `Note` with `# noqa: F401`.** The import *side
   effect* registers tables on `Base.metadata`. Without them `target_metadata` is empty and
   `alembic revision --autogenerate` generates a migration that **DROPS every table**. Ruff
   flags them as unused; `ruff --fix` will delete them. This has already broken once.

3. **Never re-add `Base.metadata.create_all()` to `main.py`.** Alembic owns the schema.
   `create_all` masked the fact that migrations were broken for the entire life of the project.
   Tests may use `create_all` on their own engine — that's the one exception.

4. **`alembic.ini` has a blank `sqlalchemy.url`.** `env.py` sets it from `settings.database_url`
   via `set_main_option(...)`. Keep the `.replace("%", "%%")` — configparser treats `%` as
   interpolation syntax and Postgres passwords will contain it.

5. **`jwt_secret_key` has no default in `Settings`.** A missing value must crash at startup.
   Never add a fallback — a default secret is how a test key ends up signing real tokens.

6. **If you `import` it, declare it in `pyproject.toml`.** `alembic`, `pwdlib`, `fastapi`, and
   `uvicorn` were all undeclared and got pruned the first time `uv` re-synced the environment.
   A working venv is not a dependency list. `pwdlib` needs the `[argon2]` extra —
   `PasswordHash.recommended()` returns an Argon2 hasher.

7. **Refactors must not change behavior.** All 7 tests must pass *unchanged* after a
   restructure, and the OpenAPI paths must match. If a test needs editing, a behavior change
   snuck in — split it into its own commit.

## Conventions

- `BaseSchema` (`schemas/base.py`) sets `from_attributes`, `alias_generator=to_camel`,
  `populate_by_name`, `extra="forbid"`. Responses are camelCase (`accessToken`, `allNotes`).
- Ownership is enforced **in the `WHERE` clause** (`Note.user_id == user_id`), not
  fetch-then-compare. This is atomic and race-free — don't "simplify" it.
- `login` returns identical errors for unknown user and wrong password. Deliberate: prevents
  user enumeration.
- `signup` keeps both the Python duplicate check *and* the DB unique constraint. The check
  gives a clean error; the constraint closes the race. After `IntegrityError`,
  `session.rollback()` is mandatory or the rest of the request fails with
  `PendingRollbackError`.
- Models use `if TYPE_CHECKING:` imports so `Mapped["Note"]` forward refs resolve without a
  runtime cycle.
- Always read an autogenerated migration before applying it. It's a draft.

## Current status

Tasks 1–5 complete (test isolation, Alembic ownership, config, unique constraint, router
split). **Task 6 (service layer) is in progress:**

- Done: `services/exceptions.py`, `services/notes.py` (`NoteService`), `get_note_service`
  provider, exception handlers in `main.py`, and `add_note` / `get_all_notes` wired up.
- **Remaining:** `update_note` and `delete_note` in `endpoints/notes.py` still contain inline
  SQL and `HTTPException` — move them onto `NoteService.update` / `.delete` (which already
  exist and raise `NotFound`). Then delete the now-unused `update`, `delete`, `Note`,
  `Session`, `get_session`, `HTTPException` imports from that module.
- **Then:** create `services/auth.py` with `AuthService` (`signup` → `AlreadyExists`,
  `login` → `InvalidCredentials`, returns token pair) and slim down `endpoints/auth.py`.
- **Payoff to demonstrate:** a service-level unit test that needs no `TestClient` —
  `pytest.raises(AlreadyExists)` around a duplicate `signup`.

Do **not** add a repository layer — with four queries it's ceremony. Do **not** change response
shapes (e.g. `UpdatedNotes.updated_rows`) during the extraction.

## Known issues (not yet addressed)

- The real JWT secret is in git history at commit `eed96a2` (`.env.example`). Rotate it if this
  repo is or becomes public — a later commit removing it does not unpublish it.
- `UpdatedNotes` exposes `updated_rows`, a SQLAlchemy `rowcount`, in the public API.
  `DELETE` should be `204`; `PUT` should return the updated resource.
- `README.md` documents an `owner_id` field that `NoteItem` doesn't return.
- `mypy` and `ruff` are in main `dependencies`; they belong in the `dev` group.
- `LoginResponse` redefines `model_config` and aliases that `BaseSchema` already provides.
- No pagination on `GET /notes`.
- `health` is `async def` while DB endpoints are `def`. That's correct — SQLAlchemy here is
  synchronous, and blocking inside `async def` would freeze the event loop. Don't "fix" it.

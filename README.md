# Smart HRM

A Human Resource Management API rebuilt with FastAPI, SQLAlchemy 2.x and Pydantic v2. The active implementation branch is feat/hrm-core-rebuild.

> Status: core rebuild in progress. This repository is not yet production-certified. See docs/REBUILD_NOTES.md for scope and release blockers.

## Current API scope

- Tenant-aware JWT login
- Organization-scoped employee listing, retrieval and HR-admin creation
- Employee-linked attendance check-in
- Liveness and database-readiness endpoints
- Alembic initial schema migration

## Technology

Python 3.11+, FastAPI, SQLAlchemy 2.x, Pydantic Settings, PostgreSQL, SQLite for tests, Argon2 password hashing, PyJWT, Alembic, pytest and Ruff.

## Local setup

1. Create a virtual environment.
2. Copy .env.example to .env.
3. Set JWT_SECRET_KEY to a unique random secret of at least 32 bytes.
4. Install development dependencies: pip install -e ".[dev]".
5. Apply schema: alembic upgrade head.
6. Create the first HR admin: python -m scripts.bootstrap_admin --organization "Example Org" --username admin --email admin@example.com.
7. Run tests: pytest -q.
8. Run lint: ruff check .
9. Start API: uvicorn app.main:app --reload.
10. Open /docs for OpenAPI documentation.

## PostgreSQL with Docker Compose

Set POSTGRES_PASSWORD and JWT_SECRET_KEY in .env, then run docker compose up --build. The API service applies the Alembic migration before starting in this single-instance local Compose setup. For production or multiple API replicas, run migrations as a controlled release job rather than concurrently at every replica startup.

## Configuration and security

See .env.example. Never commit .env, credentials or production secrets. Restrict CORS_ORIGINS to trusted frontend origins. Use a managed secrets store and rotate signing keys under a documented procedure in production.

## API routes

| Method | Route | Purpose |
|---|---|---|
| POST | /api/v1/auth/login | Authenticate using organization ID, username and password |
| GET | /api/v1/employees | List employees in authenticated organization |
| POST | /api/v1/employees | HR-admin employee creation |
| GET | /api/v1/employees/{employee_id} | Tenant-scoped employee detail |
| POST | /api/v1/attendance/check-in | Check in as the linked employee |
| GET | /health/live | Liveness |
| GET | /health/ready | Database readiness |

## Bootstrap

There is deliberately no public endpoint for creating the first administrator. Use the interactive bootstrap script only after applying migrations. Restrict shell/database access to trusted operators.

## Engineering notes

- Tenant-owned employee and attendance operations are scoped by organization ID.
- Attendance derives employee identity from the authenticated account, not a client-supplied employee ID.
- The current release does not yet include refresh-token rotation, MFA, login throttling, audit-event persistence, payroll, leave, shifts, recruitment or frontend modules.
- Healthcare-oriented legacy root files are not imported by the new app package and are pending owner-reviewed cleanup.

Read [the rebuild notes](docs/REBUILD_NOTES.md) before use.

## License

Add an explicit license before accepting external contributions or redistribution.

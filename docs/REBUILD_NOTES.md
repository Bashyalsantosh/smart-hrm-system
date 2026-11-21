# HRM core rebuild notes

This branch introduces a clean HRM application package under app/. Healthcare-oriented root-level legacy fragments are not imported by the new app. They remain in the repository for review and should be archived or removed in a separately reviewed cleanup.

## Implemented

- FastAPI application with versioned routers.
- Organization-scoped employee records and users.
- HR role gate for employee creation.
- Argon2 password hashing through pwdlib.
- JWT access tokens with required claims and an explicit algorithm allowlist.
- Tenant identifier required at login to disambiguate organization-local usernames.
- Authenticated attendance check-in tied to the logged-in user's employee record.
- Liveness and database-readiness endpoints.
- Alembic initial schema migration.
- Interactive command-line bootstrap for the first HR administrator; no public registration endpoint.
- SQLite API test fixture and regression tests.
- Ruff configuration, GitHub Actions CI, Dockerfile and PostgreSQL Compose service.

## Known limitations — not production complete

- No refresh-token rotation, password reset, MFA, login throttling or account lockout.
- No persistent audit-event store, payroll, leave, shifts, recruitment, document upload or frontend.
- No cursor pagination or advanced filtering; employee list is capped at 200.
- Attendance duplicate requests are protected by a database uniqueness constraint; multi-worker load/concurrency tests remain required.
- JWT signing-key rotation and managed secret delivery need deployment procedures.
- No production observability, backup/restore drill or incident runbook.
- CI workflow has been authored but its result must be checked after GitHub runs it.
- The GitHub file-writing connector does not execute the app or tests in this environment.

## Local verification

Copy .env.example to .env, set a unique JWT_SECRET_KEY of at least 32 bytes, install with pip install -e ".[dev]", run alembic upgrade head, then pytest -q and ruff check .. Start with uvicorn app.main:app --reload.

For Compose, configure POSTGRES_PASSWORD and JWT_SECRET_KEY in .env. The Compose command runs migrations before starting one API instance. Production multi-replica deployments should use a separate migration job and managed secrets.

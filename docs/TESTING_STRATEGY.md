# Testing strategy

No automated test suite was visible in the reviewed root inventory. This document defines required coverage; it does not claim tests currently pass.

## Unit tests

- Password hashing and verification.
- Token creation and validation.
- Role-to-permission mapping.
- Employee ID validation/generation.
- Attendance state transitions and duplicate requests.
- Leave balance and approval rules.
- Payroll calculations using Decimal and boundary cases.

## API and integration tests

- Login success, invalid password, inactive user and unknown user.
- Missing, malformed, expired and revoked token behavior.
- Employee CRUD validation and permissions.
- Attendance check-in/check-out, duplicate submissions and invalid transitions.
- Leave submission, approval and rejection.
- Tenant A cannot read or mutate Tenant B records.
- Database constraints and transaction behavior.

## Security regression tests

- Employee cannot elevate role through request payload.
- Employee cannot alter another employee's attendance.
- HR role cannot access an unassigned tenant.
- Unauthenticated requests return 401.
- Authenticated but unauthorized requests return 403.
- Sensitive fields are excluded from normal API responses and logs.
- Login throttling works under repeated failures.

## Data and migration tests

- Fresh migration from an empty database.
- Upgrade from prior migration.
- Unique constraints and foreign keys.
- UTC persistence and timezone display.
- Backup restore in a disposable environment.

## Performance tests

Establish a measured baseline before setting SLOs. Test representative read/write mixes, concurrent attendance submissions, large employee lists, report generation and database connection saturation. Record p50/p95/p99 latency, throughput, error rate and resource use.

## Suggested tooling

pytest, FastAPI TestClient or HTTPX, pytest-cov, Ruff, mypy or Pyright, Bandit or Semgrep, pip-audit, and optionally Testcontainers.

## Suggested commands after the dependency manifest exists

    python -m compileall -q app
    pytest -q
    pytest --cov=app --cov-report=term-missing
    ruff check .
    ruff format --check .
    pip-audit

Do not create a green CI badge until CI installs pinned dependencies, runs lint/type checks, applies migrations to a disposable database and passes tests.

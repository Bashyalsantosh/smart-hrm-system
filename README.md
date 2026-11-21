# Smart HRM System

A Human Resource Management System project with a Python/FastAPI implementation direction.

> **Audit notice — 2026-11-21:** The reviewed repository snapshot is an incomplete scaffold and is not verified as production-ready. It contains FastAPI, SQLAlchemy-style models, password hashing and role/permission code, but also healthcare-domain entities and inconsistent Python import paths. Read the [code audit](docs/CODE_AUDIT.md) before running or deploying it.

## Verified implementation signals

These are source-code observations, not claims that complete workflows have passed integration testing:

- FastAPI application and root/health endpoints in `main.py`.
- Pydantic Settings configuration for database URL, secret key, JWT algorithm and access-token expiry in `config.py`.
- Bcrypt password hashing and verification helpers in `Security.py`.
- Login route calling an authentication service and access-token creation in `login.py`.
- Role/permission mapping in `rbac.py`.
- SQLAlchemy-style user and attendance model fragments in `Service.py` and `atten.py`.

## Technology signals

| Area | Evidence |
|---|---|
| API | FastAPI |
| Configuration/validation | Pydantic Settings, Pydantic |
| ORM | SQLAlchemy |
| Authentication | JWT-related imports; bcrypt via Passlib |
| Database | Configured through `DATABASE_URL`; production database setup not verified |
| Containers | `compose.yml` is currently empty |

## Important scope warning

Some files describe a hospital system (patients, doctors, nurses, laboratories and pharmacy), while this repository is named Smart HRM. Imports also reference an `app/` package whose complete tree was not present in the reviewed root-level inventory. Confirm the intended product domain and reconcile the package layout before adding features.

Do not use this repository with real employee or patient data until authentication, authorization, tenant isolation, migrations, audit logging, data protection and tests have been implemented and independently verified.

## Engineering documentation

- [Code audit and findings](docs/CODE_AUDIT.md)
- [Architecture baseline and target design](docs/ARCHITECTURE.md)
- [Security review and remediation checklist](docs/SECURITY_REVIEW.md)
- [Testing strategy](docs/TESTING_STRATEGY.md)
- [Production-readiness roadmap](docs/PRODUCTION_ROADMAP.md)

## Local setup

A verified end-to-end setup cannot yet be documented: the reviewed snapshot did not include a dependency manifest/lockfile, complete package tree, database migrations or populated Compose configuration.

Before publishing run instructions, add and verify:
1. Supported Python version and pinned dependencies.
2. Environment variable template with safe local defaults.
3. Database provisioning and migration steps.
4. Development server command.
5. Test, lint and type-check commands.

## Security

Never commit `.env`, credentials, private keys, production database URLs or personal data. Use deployment secrets or a secrets manager. Rotate any credential that may have been exposed.

## Contributing

Read the audit and roadmap before implementing features. Keep changes small, test business rules and authorization boundaries, and update API/architecture documentation when contracts change.

## License

No license was verified in the reviewed repository snapshot. Until the owner adds a license, reuse and redistribution permissions should not be assumed.

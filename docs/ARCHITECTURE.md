# Architecture baseline and target design

## Observed baseline

Visible source indicates Python/FastAPI, Pydantic Settings, SQLAlchemy-style models, Passlib bcrypt and JWT-related authentication imports. The entry point imports an employee model from an app package, while other snippets use different import roots and healthcare-specific entities. The executable architecture is not yet established.

## Assumed product boundary

This target design assumes the intended product is Human Resource Management. Confirm that assumption and remove patient/clinical concepts if HRM is correct.

Recommended modules:
- Identity and access management
- Organizations and departments
- Employees and employment records
- Attendance and shifts
- Leave and approvals
- Payroll (only after jurisdiction-specific rules are defined)
- Recruitment (optional)
- Audit, reporting and notifications

## Recommended architecture: modular monolith

Clients (web/mobile) -> TLS reverse proxy -> FastAPI API/versioned routers -> authentication and authorization -> application services -> domain modules -> SQLAlchemy repositories -> PostgreSQL.

Optional background worker/queue for notifications, scheduled tasks and report generation. Add centralized structured logs, metrics and traces.

Start with a modular monolith; do not introduce microservices before operational needs justify them.

## Suggested package layout

    app/
      main.py
      api/
        deps.py
        v1/
          router.py
          endpoints/
      core/
        config.py
        database.py
        security.py
        logging.py
      modules/
        organizations/
        employees/
        attendance/
        leave/
        payroll/
        audit/
      tests/
        unit/
        integration/
        api/
    alembic/
    docs/

Keep HTTP concerns in routers, business rules in services, persistence in models/repositories and contracts in schemas. Use one declarative Base and avoid circular imports.

## Design rules

- Use PostgreSQL constraints for uniqueness and referential integrity.
- Store timestamps in UTC; convert at presentation boundaries.
- Represent money with fixed-precision Decimal/Numeric, never binary floating point.
- Use explicit enums and validated state transitions.
- Enforce tenant scope server-side on every read and write.
- Use Alembic migrations; do not rely on ad-hoc production table creation.
- Make check-in/check-out idempotent and concurrency-safe.
- Add pagination and bounded query limits.
- Version payroll rules and audit changes.

## Multi-tenancy

Every tenant-owned row should carry an organization identifier. Derive tenant context from the authenticated principal, not an arbitrary client-supplied ID. Scope every query, include tenant IDs in tenant-local unique constraints and test cross-tenant denial. PostgreSQL Row-Level Security can provide defense in depth.

## API conventions

Version under /api/v1; use consistent resources and HTTP methods; return stable sanitized errors; use 401 for unauthenticated and 403 for unauthorized requests; add request IDs and structured logs; document pagination and validation in OpenAPI.

## Production topology

A reasonable first deployment is managed PostgreSQL, stateless API instances, TLS-terminating proxy/load balancer, managed secrets, private object storage, centralized observability, automated backups and tested restore procedures. Do not claim high availability or scalability until load and failover tests demonstrate it.

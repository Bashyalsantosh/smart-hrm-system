# Production-readiness roadmap

The order is intentional: domain and repository integrity must precede security hardening and feature expansion. Estimate dates after confirming scope and inventory.

## Phase 0 — product and repository integrity

- [ ] Confirm whether this is HRM or hospital management.
- [ ] Inventory tracked files and remove unrelated modules.
- [ ] Adopt one lowercase Python package layout.
- [ ] Make imports resolve from a clean checkout.
- [ ] Add supported Python version, pinned dependencies and environment template.
- [ ] Make local startup reproducible.

Exit gate: clean checkout installs and starts; domain model and README agree.

## Phase 1 — core platform

- [ ] Centralize settings and validate secrets.
- [ ] Centralize SQLAlchemy Base and session lifecycle.
- [ ] Add Alembic migrations and PostgreSQL integration.
- [ ] Standardize API versioning, error handling and structured logs.
- [ ] Implement organization and employee models, schemas, services and routes.
- [ ] Add constraints and pagination.

Exit gate: core API integration tests pass.

## Phase 2 — security and authorization

- [ ] Complete authentication lifecycle and token validation.
- [ ] Implement HRM-specific role/permission policy.
- [ ] Enforce tenant and object-level authorization.
- [ ] Add throttling, CORS, TLS and secrets management.
- [ ] Add audit trail for sensitive actions.
- [ ] Close Priority 0 security checklist.

Exit gate: authorization matrix and cross-tenant regression tests pass.

## Phase 3 — HR workflows

- [ ] Attendance and shift management.
- [ ] Leave request and approval workflow.
- [ ] Payroll only after tax, benefits and approval requirements are specified.
- [ ] Reporting and document generation.
- [ ] Notifications and scheduled tasks.

Exit gate: workflow acceptance, audit and reconciliation tests pass.

## Phase 4 — reliability and operations

- [ ] CI for lint, tests, migrations and dependency scanning.
- [ ] Structured logs, metrics, traces and request correlation IDs.
- [ ] Liveness/readiness probes.
- [ ] Database backup and restore drill.
- [ ] Load and concurrency tests.
- [ ] Deployment rollback procedure and incident runbook.

Exit gate: release checklist and operational evidence recorded.

## Phase 5 — controlled release

- [ ] Deploy to staging with synthetic data.
- [ ] Perform security review and user acceptance testing.
- [ ] Validate restore, rollback and monitoring alerts.
- [ ] Pilot with a limited organization.
- [ ] Review incidents and performance before wider rollout.

## Definition of done

A feature is complete only when business rules, authorization, validation, database constraints, tests, documentation, audit behavior and operational monitoring are in place.

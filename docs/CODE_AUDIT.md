# Code audit

Reviewed 2026-11-21. Scope: visible root files README.md, main.py, config.py, Auth.py, Security.py, Service.py, atten.py, login.py, patient.py, rbac.py, router.py, serviceauth.py and compose.yml. Static review only: no install, runtime test, database test or penetration test was performed.

## Executive finding

This repository is not currently verifiably production-ready. It appears to be an incomplete Python/FastAPI scaffold with a serious product-domain mismatch: the repository is named Smart HRM, but several files model a hospital system.

## Findings

| ID | Severity | Finding | Evidence and impact |
|---|---|---|---|
| AUD-01 | Critical | HRM/healthcare domain mismatch | Service.py defines hospital users and doctor/nurse/lab/pharmacist roles; patient.py defines patient records; rbac.py grants patient, EMR, lab and pharmacy permissions. |
| AUD-02 | Critical | Inconsistent package structure | main.py imports app.modules.employees.model; other files import app.core, app.models, app.database and app.schemas modules. The visible root inventory is flat and does not show this package tree. Clean-checkout startup is unverified. |
| AUD-03 | High | Attendance endpoint lacks visible authentication | router.py accepts employee_id and changes attendance without a visible authenticated-user dependency or object-level permission check. |
| AUD-04 | High | Tenant isolation is not demonstrated | Service.py has hospital_id, but the attendance lookup shown filters only by employee and date. Every read/write must enforce organization scope. |
| AUD-05 | High | JWT controls cannot be verified | login.py calls token creation, but implementation was not in the reviewed files. Expiry, issuer/audience, algorithm allowlist, refresh/revocation and key rotation remain unverified. |
| AUD-06 | High | Configuration contract incomplete | config.py requires DATABASE_URL and SECRET_KEY, but no environment template, dependency manifest or documented secret-rotation process was visible. |
| AUD-07 | High | Suspicious SQLAlchemy timestamp default | atten.py uses server_default=DateTime, which is a SQLAlchemy type, not an explicit database timestamp expression. Replace and test. |
| AUD-08 | High | Attendance check-in race risk | The visible read-then-write sequence can race under concurrent requests. Enforce atomic/idempotent behavior and handle uniqueness conflicts. |
| AUD-09 | Medium | Multiple Base import paths | atten.py imports app.database.database.Base while other files use app.core.database.Base. This may split metadata or fail at import time. |
| AUD-10 | Medium | Inconsistent naming | Auth.py, Security.py, Service.py and atten.py use inconsistent naming. Adopt a conventional lowercase package layout. |
| AUD-11 | Medium | Entry point incomplete in visible code | main.py shows root and health endpoints only; router registration, exception handling, lifecycle and readiness are not shown. |
| AUD-12 | Medium | Build/test setup absent in reviewed inventory | No requirements/lock file, tests, migrations or populated Compose configuration were visible. Reproducible builds are not established. |
| AUD-13 | Medium | Health endpoint is not readiness | /health returns healthy without checking database or dependencies. Separate liveness and readiness checks. |
| AUD-14 | Medium | Patient data is out of scope for HRM | patient.py includes date of birth, blood group, phone, address and emergency contact fields. Remove if this is an HRM product. |

## Immediate decisions

1. Confirm whether the product is HRM or Hospital Management. Do not mix the two domains.
2. Reconcile the Python package tree and all imports.
3. Use one SQLAlchemy Base, one session lifecycle and database migrations.
4. Require authentication and object-level authorization on all employee/attendance operations.
5. Add organization scoping to every query if multi-tenant operation is intended.
6. Add automated tests before claiming workflows are complete.

## Not verified

Runtime startup, database migrations, JWT internals, complete routes/services, frontend, dependency versions, container build, deployment, load behavior, backup/restore and commit-history secret exposure were not tested.

## Audit closure criteria

- Confirmed domain and matching entities/roles.
- All imports resolve from a clean checkout.
- Reproducible dependency manifest and migration workflow.
- Authenticated, tenant-scoped HR endpoints.
- Unit, integration and authorization tests.
- Passing CI and documented security review.

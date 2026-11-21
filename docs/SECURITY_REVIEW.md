# Security review and remediation checklist

This is a code-informed remediation plan, not a security certification.

## Priority 0 — before real employee data

- [ ] Confirm HRM versus healthcare scope; remove unrelated patient data and clinical permissions if HRM is intended.
- [ ] Require authenticated principals for employee, attendance, leave and payroll endpoints.
- [ ] Enforce object-level authorization for every record.
- [ ] Enforce tenant isolation on every query and mutation.
- [ ] Validate JWT signature, expiry, issuer, audience and an explicit allowed algorithm.
- [ ] Keep secrets outside source control; use strong random keys and a rotation procedure.
- [ ] Add login throttling and monitoring for repeated failures.
- [ ] Never log passwords, access tokens or sensitive employee information.
- [ ] Require TLS outside local development.
- [ ] Define retention, access, export and deletion rules for employee records.

## Priority 1 — application hardening

- [ ] Review password hashing parameters and password reset flow.
- [ ] Add refresh-token rotation/revocation if refresh tokens are used.
- [ ] Add CSRF protection if browser cookies carry authentication.
- [ ] Restrict CORS to explicit trusted origins.
- [ ] Apply request size limits, schema validation and rate limits.
- [ ] Use explicit request schemas to prevent mass assignment.
- [ ] Add audit events for login, permission changes, employee record access and payroll changes.
- [ ] Protect uploaded files with type/size validation, malware scanning and private storage.
- [ ] Sanitize errors and keep stack traces server-side.
- [ ] Scan dependencies and container images.

## Priority 2 — infrastructure

- [ ] Use least-privilege database credentials and network restrictions.
- [ ] Encrypt backups and document storage.
- [ ] Test backup restoration.
- [ ] Separate development, test and production environments.
- [ ] Centralize security logs and alert on suspicious access.
- [ ] Define incident response and credential-compromise procedures.
- [ ] Review security headers and update dependencies regularly.

## Source-specific observations

1. The visible attendance check-in handler accepts an employee ID and does not show an authenticated user dependency. Bind identity to the principal or enforce explicit permission before mutation.
2. The attendance query does not show organization scoping.
3. JWT creation is called by the login route, but its implementation was not in the reviewed files. Verify expiry, issuer, audience, algorithm allowlist, key management and revocation.
4. Configuration requires a secret but does not document strength or rotation.
5. patient.py contains sensitive health-related fields inconsistent with an HRM product.

## Release gate

Do not deploy with real data until all Priority 0 items are closed, automated tests prove cross-user and cross-tenant access is denied, secrets are scanned and an independent reviewer signs off.

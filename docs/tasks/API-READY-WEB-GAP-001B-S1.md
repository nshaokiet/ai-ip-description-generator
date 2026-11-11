# API-READY-WEB-GAP-001B-S1 — local transport and authentication

Version 0.1.0, 2026-11-11. Implementation candidate; independent review and
separate Human merge decision required. Human's 2026-11-11 implementation order
authorizes D-GAP-01/D-GAP-03 for S1 only. D-GAP-02, R0/R1, product routes,
providers, deployment and merge are not authorized.

## Boundary

The dedicated FastAPI factory is disabled unless explicitly configured with a
live protected control service. The released backend, public demo and Next app
route tree are unchanged. Only the opt-in Next custom HTTPS server owns the
private `/product-web` authentication page and `/api/product-web/v1/session`
(GET/POST/DELETE) and `/session/bootstrap` (POST) proxy paths. Other paths are 404.
The small inert authentication page is served by that custom server; it is not
registered as a released/static-export Next page. No document functionality exists.

## Operator prerequisites and launch

Use the existing locked Python/Node dependencies and a normal frontend build.
Provision an empty owner-private state parent and operator-owned certificate/key
in an owner-private directory. No path component may be a symlink/reparse point.
Windows ACLs must grant access only to the current account; Unix directories must
be 0700 and files 0600. The containing runtime directory must be in a stable,
operator-controlled location, not a shared writable directory. The launcher does
not provision certificates, install a CA or alter a trust store. The certificate
must be valid for DNS SAN `localhost`, match the key and be trusted by the operator's
browser. Missing/mismatched/insecure material denies startup.

```text
python -m backend.app.local_product_web --enable --state-parent <private-empty-directory> --cert <certificate.pem> --key <private.pem>
```

Open `https://localhost:3443/product-web` and request pairing. In the trusted host
terminal, locate the new instance's `host.json` inside the private state parent
(do not print its contents), compare the displayed selector, then run:

```text
python -m backend.app.services.product_web_host_control approve <instance>/host.json <selector>
```

Approval does not log in. Complete login in the original browser context. Host
`revoke-all <instance>/host.json` revokes all sessions; `shutdown` on the same
protected channel revokes and stops the dedicated host. Control keys never appear
in CLI arguments. The Next process receives only its separate private proxy file.

## Enforced controls

- Exact loopback peer, backend Host, frontend Host/Origin, Fetch Metadata,
  private proxy credential and bounded request/header checks. Incoming forwarding,
  internal-auth and proxy-auth headers are rejected at the public side; the proxy
  forwards a fixed header/path/method allowlist. No credentialed CORS.
- Real Linux AF_UNIX peer UID/socket checks or Windows owner-only Named Pipe DACL
  readback, remote-client rejection and TokenUser impersonation checks. Per-connection
  random nonce, instance-bound HMAC, 5-second challenge and 4-KiB framing; no HTTP approval.
- Eight pending logins, 60-second absolute lifetime, 12 allocations/minute; two
  authenticated sessions, 1800-second absolute lifetime. Reads do not renew TTL.
  Login consumes approval and rotates cookie/CSRF, with separate server owners.
  Logout/host revocation clears authority. Single-use login credentials cannot replay.
- Secure/HttpOnly/SameSite=Strict host-only `__Host-` cookies, session-bound CSRF,
  no-store, inert UI, CSP and no secrets in URLs, logs or browser persistent storage.

The current OS account is trusted. This is not isolation from same-account malware
or privileged administrators, and cookies are not isolated by port. Private proxy
authentication and exact Origin remain necessary. Startup requires an empty state
parent; it never deletes an existing host's files. Graceful shutdown removes only
its owned state/socket; after a crash, stale private files require operator inspection
and cleanup before restart. No session/approval is restored after a restart.

## Verification

Focused native tests: `python -m pytest tests/backend/test_product_web_*.py -q`.
They execute the current platform's actual channel and ACL/peer checks. Offline
test-only TLS certificates use an already installed OpenSSL; no network fallback.
Browser test `frontend/e2e/product-web-auth.spec.ts` starts the same launcher and
approves via the real operator CLI. Only that pinned localhost test context permits
the ephemeral certificate. Existing CI discovers both backend and browser tests;
Linux results belong to exact-head hosted evidence, not Windows test extrapolation.
Python SDK/transport tripwires and the browser egress guard record unexpected activity.

Local Windows 11/Python 3.12.10/Node 24.18.0 candidate verification: 34 S1 backend
cases plus 7 existing provider-tripwire cases PASS; 3 real HTTPS browser cases PASS
(independent sessions, proxy negatives, host restart); locked frontend lint,
typecheck and build PASS. Unexpected Python client construction/API/egress and
browser egress counters were zero. Native tests read the actual current-user pipe
DACL and impersonated TokenUser; no second OS account or physical remote host was
used for penetration testing. Linux native/socket/browser results must be checked
in exact-head CI; local Windows success is not cross-platform acceptance.

API budget USD 0; provider NOT_RUN; Claims runtime DISABLED; semantic readiness
NOT_DETERMINED; live spend enforcement NOT_IMPLEMENTED. No fixture admission,
upload, parsing, custody, patent review, generation, render or download is added.

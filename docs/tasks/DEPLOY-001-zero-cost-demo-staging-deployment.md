# DEPLOY-001 — Zero-Cost Demo/Staging Deployment

| Field | Value |
|---|---|
| Version | 0.2.0 |
| Status | **AUTHORIZED — PLATFORM DECISION REQUIRED BEFORE CODE/DEPLOY** |
| Owner | ChatGPT/Codex under AGENTS.md standing delegation |
| Baseline | `ed16fbc24d0ee06d7c2294a49bf243a448e6df87` |
| Human roadmap registration | `HUMAN-DEPLOY-001-ROADMAP-REGISTRATION-2026-09-29` |
| Implementation authorization | **GRANTED** — `HUMAN-DEPLOY-001-IMPLEMENTATION-2026-10-01` |
| Independent reviewer | Gemini 3.1 Pro High when implementation is authorized |
| Project classification | **MVP COMPLETE — LOCAL/SYNTHETIC** |

## Purpose

Provide a zero-cost demo/staging deployment path that can expose the existing application through a public HTTPS URL for demonstrations using synthetic/demo inputs only.

DEPLOY-001 is explicitly **not** a production deployment task and does not resolve SEC-001 / BLK-003.

## Intended functions

- Publish a browser-accessible demo/staging URL.
- Connect the existing Next.js frontend to the existing FastAPI backend in a hosted demo environment.
- Provide basic deployment health verification and a reproducible deployment/runbook.
- Preserve the current synthetic/demo-only boundary and visible drafting/legal disclaimers.
- Use zero-cost hosting tiers or equivalent no-cost infrastructure only, subject to a separate Human platform decision.

## Scope boundaries

DEPLOY-001 does **not** authorize:

- a specific hosting platform (Vercel, Railway, Render, Cloudflare, or otherwise);
- paid hosting, paid provider/API calls, or new recurring cost;
- OpenAI live/provider validation or EVAL-001 PRODUCT_RUNTIME;
- production release or production-readiness claims;
- real, confidential, unpublished, or sensitive research documents;
- production authentication, tenant isolation, private storage, retention/deletion acceptance, or BLK-003 closure;
- Claims or legal/filing automation.

Any platform selection, paid service, security-policy change, real-data use, or production deployment is a Section 19 Human decision.

## Recommended sequencing

Roadmap position: after P1-006 for a polished public demo.

This sequencing recommendation is now satisfied. DEPLOY-001 implementation is Human-authorized under `HUMAN-DEPLOY-001-IMPLEMENTATION-2026-10-01`, but code/deploy work remains blocked until the Human selects the hosting platform as required by the scope boundary.

## Future implementation acceptance criteria

When implementation is separately authorized, it should demonstrate all of the following:

1. A public HTTPS demo/staging URL is available.
2. Frontend and backend are reachable through the documented demo architecture.
3. Health checks and the intended synthetic/demo flow work without exposing local-only secrets.
4. No secrets, API keys, confidential papers or generated sensitive data are committed.
5. Hosting cost is zero under the approved platform/tier; any cost change stops work.
6. Demo accepts synthetic/demo content only and communicates that real/confidential research data is not authorized.
7. Provider/API calls remain disabled unless separately authorized.
8. Deployment configuration and rollback/redeployment instructions are documented.
9. Existing offline CI/regression remains green.
10. Independent Gemini 3.1 Pro High review and required CI pass on the final implementation SHA before merge.
11. Demo/staging is not labeled production-ready and does not close BLK-003.
12. A post-deploy verification records the actual public URL and exact deployed revision.

## Current blockers / prerequisites

- Implementation authorization: **GRANTED** under `HUMAN-DEPLOY-001-IMPLEMENTATION-2026-10-01`.
- Hosting platform: **TBD — Section 19 Human decision required before code/deploy implementation**.
- BLK-003: **OPEN**; does not block a synthetic/demo-only staging design, but blocks production/real-data use.
- Provider authorization: **NOT GRANTED**; budget **0**.
- EVAL-001 PRODUCT_RUNTIME: **DEFERRED — AWAITING FUNDING**.

## Current state

DEPLOY-001 is **AUTHORIZED — PLATFORM DECISION REQUIRED BEFORE CODE/DEPLOY**. Governance preparation may proceed on `feat/deploy-001-demo-staging`, but no platform-specific deployment configuration, public URL, provider call, production approval or real-data authorization is created until the Human explicitly selects a hosting platform.

Authorization scope remains limited to a zero-cost synthetic/demo-only staging deployment. The authorization does not approve production, paid services, provider/API calls, real/confidential research data, BLK-003 closure, Claims, or EVAL-001 PRODUCT_RUNTIME.


## Authorization record — 01/10/2026

- Human instruction: continue with the next roadmap task after P1-006 closeout.
- Authorization reference: `HUMAN-DEPLOY-001-IMPLEMENTATION-2026-10-01`.
- Authorized baseline: `ed16fbc24d0ee06d7c2294a49bf243a448e6df87`.
- Implementation branch: `feat/deploy-001-demo-staging`.
- Platform selection remains a separate Section 19 Human decision and is **not inferred** from this authorization.
- No deployment code/configuration has been created at this authorization checkpoint.

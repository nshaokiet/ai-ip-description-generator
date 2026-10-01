# DEPLOY-001 — Zero-Cost Demo/Staging Deployment

| Field | Value |
|---|---|
| Version | 0.2.0 |
| Status | **IMPLEMENTATION STARTED — CODEX HANDOFF / RENDER CONNECTION REQUIRED FOR LIVE DEPLOY** |
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
- Hosting platform: **Render — selected by Human on 01/10/2026** under `HUMAN-DEPLOY-001-PLATFORM-RENDER-2026-10-01`.
- BLK-003: **OPEN**; does not block a synthetic/demo-only staging design, but blocks production/real-data use.
- Provider authorization: **NOT GRANTED**; budget **0**.
- EVAL-001 PRODUCT_RUNTIME: **DEFERRED — AWAITING FUNDING**.

## Current state

DEPLOY-001 is **AUTHORIZED — RENDER SELECTED; IMPLEMENTATION HANDOFF READY**. Platform-specific implementation may now proceed on `feat/deploy-001-demo-staging` using Render only. No public URL, provider call, production approval or real-data authorization is claimed until verified deployment evidence exists.

Authorization scope remains limited to a zero-cost synthetic/demo-only staging deployment. The authorization does not approve production, paid services, provider/API calls, real/confidential research data, BLK-003 closure, Claims, or EVAL-001 PRODUCT_RUNTIME.


## Authorization record — 01/10/2026

- Human instruction: continue with the next roadmap task after P1-006 closeout.
- Authorization reference: `HUMAN-DEPLOY-001-IMPLEMENTATION-2026-10-01`.
- Authorized baseline: `ed16fbc24d0ee06d7c2294a49bf243a448e6df87`.
- Implementation branch: `feat/deploy-001-demo-staging`.
- Platform decision: **Render**, explicitly selected by the Human under `HUMAN-DEPLOY-001-PLATFORM-RENDER-2026-10-01`.
- No deployment code/configuration had been created before this platform-selection checkpoint.


## Platform decision — Render

- Decision reference: `HUMAN-DEPLOY-001-PLATFORM-RENDER-2026-10-01`.
- Selected platform: **Render**.
- Target architecture: a **Render Static Site** for the exported Next.js frontend plus a single **Render Free Web Service** for the FastAPI synthetic/demo backend, unless implementation evidence shows a documented Render limitation that requires a narrower alternative.
- The hosted backend must remain deterministic/offline and must not instantiate or call OpenAI/provider runtimes.
- The public demo must clearly identify itself as synthetic/demo staging and must include a technical guard that prevents accidental real/confidential document use rather than relying only on warning text.
- Prefer same-origin or tightly restricted origin routing. Do not use wildcard CORS.
- Free-tier limitations are acceptable for staging, including spin-down/cold-start behavior and ephemeral filesystem, but must be documented as demo constraints rather than production guarantees.
- If Render Blueprint wiring cannot express a safe dynamic frontend/backend URL relationship, document the minimum manual Dashboard wiring step instead of hard-coding or guessing an unverified public hostname.


## Implementation start — 01/10/2026

- Human instruction: begin the Render deployment work now.
- Code implementation owner remains **Codex** under AGENTS.md standing delegation.
- Repository implementation begins from branch head `13cebe50fe28482f84eb60f15434b32edf63fb47` on `feat/deploy-001-demo-staging`.
- Live Render service creation/deployment requires the user's Render account connection; no service or public URL is claimed before that connection and verified Render evidence exist.
- Until the fixed-SHA implementation review and merge gates are satisfied, repository work is limited to staging-safe code/config/tests/runbook and no production/provider/real-data authorization is implied.

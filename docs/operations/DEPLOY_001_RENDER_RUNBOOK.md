# DEPLOY-001 Render Demo/Staging Runbook

| Field | Value |
|---|---|
| Version | 0.1.0 |
| Status | Implementation complete — review and deployment pending |
| Task | DEPLOY-001 |
| Platform | Render |
| Authorization | `HUMAN-DEPLOY-001-IMPLEMENTATION-2026-10-01`; `HUMAN-DEPLOY-001-PLATFORM-RENDER-2026-10-01` |
| Public frontend URL | **NOT DEPLOYED / NOT RECORDED** |
| Public backend URL | **NOT DEPLOYED / NOT RECORDED** |
| Production status | **NOT PRODUCTION; BLK-003 OPEN** |

## 1. Purpose and hard boundary

This runbook deploys a public, zero-cost **synthetic demo/staging** instance. It
does not authorize production, paid services, provider/API calls, or real,
confidential, unpublished, or sensitive research data. The output remains a
draft for Human/IP-specialist review; it is not legal advice, a patentability
opinion, or filing-ready material.

Stop if Render requires a paid plan, an unapproved external service, a provider
credential, or a change to authentication/data-handling policy.

## 2. Architecture

```text
Browser
  -> Render Static Site (frontend/out)
       -> same-origin /backend/* rewrite
            -> Render Free Web Service (FastAPI demo_staging)
                 -> controlled synthetic samples only
                 -> deterministic synthetic extraction/drafting runtimes
                 -> canonical validators + real DOCX renderer
                 -> ephemeral temporary files
```

The normal local application remains unchanged. Static export is enabled only
when `RENDER_STATIC_EXPORT=1`; demo UI restrictions are enabled only when
`NEXT_PUBLIC_DEMO_STAGING=1`.

## 3. Synthetic-only enforcement

The public UI exposes two controlled actions and no arbitrary file picker:

- `synthetic-pdf-v1`
- `synthetic-docx-v1`

The backend serves these exact samples and accepts an upload only when the
sample ID, filename, media type, and SHA-256 digest match the server-issued
sample. Missing contracts are rejected with HTTP 403; modified or mismatched
samples are rejected with HTTP 422. Warning text is therefore not the only
boundary.

The staging entrypoint is `backend.app.demo_staging:app`. It injects
deterministic runtimes and sets no OpenAI key. It does not instantiate provider
runtimes or make provider/network calls during processing.

## 4. Repository pre-deployment gates

Do not connect or deploy the Blueprint until all of these are true on the exact
candidate SHA:

1. Pull-request CI is `SUCCESS`.
2. Independent Gemini 3.1 Pro High review is `PASS` on that exact SHA, with no
   unresolved blocking finding.
3. The PR is merged under the AGENTS.md merge gates.
4. The post-merge SHA and main CI are verified.
5. The Render account remains on zero-cost resources with no paid feature.

At this runbook revision those deployment gates are **pending**. No live URL is
claimed.

## 5. Blueprint resources

The repository-root `render.yaml` declares exactly:

- `ai-ip-synthetic-demo-frontend`: Render Static Site.
- `ai-ip-synthetic-demo-backend`: one Render Free Web Service in Singapore.

There is no database, persistent disk, background worker, provider credential,
or wildcard CORS configuration.

## 6. Create the Render Blueprint

After the merge/review gates are satisfied:

1. Sign in to the authorized Render account.
2. Choose **New > Blueprint**.
3. Connect the private GitHub repository
   `nshaokiet/ai-ip-description-generator` with the minimum repository access
   required by Render.
4. Select the approved merged branch (normally `main`).
5. Confirm Render detects the repository-root `render.yaml`.
6. Review both resources before applying. The backend must show **Free**; the
   frontend must show **Static Site**.
7. Confirm no database, disk, worker, secret, or `OPENAI_API_KEY` is proposed.
8. Apply only if the expected zero-dollar configuration remains visible.

Do not enter a provider/API key in the Dashboard.

## 7. Frontend build settings

The Blueprint supplies:

```text
Build command: cd frontend && npm ci && npm run build
Publish path: frontend/out
RENDER_STATIC_EXPORT=1
NEXT_PUBLIC_DEMO_STAGING=1
```

The two variables are public build controls, not credentials. The static export
must contain the visible `Synthetic Demo / Staging` label and the real/confidential
data warning.

## 8. Backend build and start settings

The Blueprint supplies:

```text
Build command: python -m pip install -r backend/requirements.txt
Start command: python -m uvicorn backend.app.demo_staging:app --host 0.0.0.0 --port $PORT
Health check: /health
Plan: free
Region: singapore
```

Keep live-test flags disabled. `AI_IP_ENABLE_LOCAL_ORCHESTRATION_API=0` is
intentional: the dedicated staging app injects its provider-free orchestration
dependencies directly.

## 9. Verify the backend before frontend wiring

Deploy the backend first. Record the exact service URL only after it exists and
passes both checks:

```text
GET https://<verified-backend-host>/health
Expected: 200 and {"status":"ok"}

GET https://<verified-backend-host>/api/demo/samples/synthetic-pdf-v1
Expected: 200, application/pdf, Cache-Control: no-store
```

Also send an ordinary multipart upload without `X-AI-IP-Demo-Sample` and verify:

```text
POST https://<verified-backend-host>/api/documents
Expected: 403, error.code = synthetic_demo_sample_required
```

Do not paste a real document into this check.

## 10. Configure the same-origin frontend rewrite

Render Blueprint variables cannot safely interpolate the provisioned backend's
public hostname into a static-site rewrite. After the backend hostname has been
verified, configure one rule on the **frontend Static Site** in the Render
Dashboard:

```text
Type: Rewrite
Source: /backend/*
Destination: https://<verified-backend-host>/*
```

Use the exact hostname displayed by Render; do not guess it and do not commit a
placeholder hostname. Save the rule, redeploy the frontend, and check the
deployed rule before continuing.

## 11. Security headers

Verify a frontend response includes the Blueprint-configured headers:

```text
Cache-Control: no-store
Permissions-Policy: camera=(), geolocation=(), microphone=()
Referrer-Policy: no-referrer
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
```

The exact `/*` header path is declared in `render.yaml`.

## 12. Public smoke test

Use only the controlled buttons in the deployed frontend:

1. Confirm the staging badge and all boundary/legal warnings are visible.
2. Confirm there is no file picker or drag/drop target.
3. Run **Use synthetic PDF demo** through analysis.
4. Edit one permitted prose field, save a new revision, validate, and export.
5. Confirm the downloaded file is a DOCX and corresponds to the validated
   selected revision.
6. Repeat the full flow with **Use synthetic DOCX demo**.
7. Confirm browser developer tools show `/backend/*` same-origin requests and no
   direct provider/API request.

Failure of either sample flow blocks URL publication and task closeout.

## 13. Provider-free verification

In Render settings and logs verify:

- no `OPENAI_API_KEY` or other provider credential exists;
- the start command targets `backend.app.demo_staging:app`;
- live-test flags are `0`;
- the exact-head automated tests still verify `synthetic_demo` /
  `deterministic_fixture_v1`, provider constructors not called, and provider
  call counters at zero;
- no provider endpoint or provider request ID appears.

The deterministic outputs demonstrate plumbing only. They do not demonstrate
live-model or semantic quality.

## 14. Storage and retention behavior

Render's free web-service filesystem is ephemeral. The application also deletes
uploaded sources after processing and uses temporary export storage. Do not
treat the filesystem as durable storage or a retention guarantee. Never upload
real/confidential data, and never use this deployment as a system of record.

## 15. Free-tier and availability constraints

Render documents that a free web service spins down after 15 minutes without
inbound traffic and can take about one minute to start again. The first demo
request may therefore be slow or temporarily fail while the backend wakes.
Free-tier usage and bandwidth limits also apply. This behavior is acceptable
only for demo/staging and is not a production availability commitment.

Before every deployment, re-check the current [Render free-tier documentation](https://render.com/docs/free).
Stop rather than enable paid capacity if the free allocation is unavailable or
exhausted.

## 16. Logging and data handling

Do not log or copy full uploaded content, generated sensitive data, credentials,
or signed URLs. The only authorized inputs are the repository-controlled
synthetic samples. Render log access must remain limited to the authorized
account/team.

## 17. Redeploy

For a reviewed follow-up revision:

1. Complete the same exact-SHA review/CI/merge gates.
2. In Render, deploy the verified commit from the approved branch.
3. Reconfirm the backend health check and frontend rewrite.
4. Repeat both sample flows and the arbitrary-upload rejection check.
5. Record the deployed commit and new evidence; do not silently reuse evidence
   from an older SHA.

## 18. Rollback

If a deployment regresses but the service can remain public safely, use Render's
rollback/redeploy control to select the last reviewed, known-good deployment.
Then repeat health, guard, headers, and both sample-flow checks. Record the
actual rolled-back SHA.

Rollback is not a substitute for review. If the known-good revision cannot be
identified or its configuration differs, disable public access instead.

## 19. Disable or remove the public demo

Immediately suspend/delete the frontend and backend resources, or disconnect
their public routes, if any of these occur:

- arbitrary uploads are accepted;
- provider calls or credentials appear;
- cost is incurred or a paid upgrade is requested;
- secret/confidential data exposure is suspected;
- the rewrite points to an unverified service;
- a blocking review/CI/security finding is discovered.

After disabling, verify both public URLs are no longer usable and preserve only
non-sensitive incident evidence. Do not delete Git history or review records.

## 20. Troubleshooting

- **Initial 502/timeout:** wait for the documented free-service cold start, then
  recheck backend `/health` before retrying the frontend.
- **Frontend 404 under `/backend/*`:** verify the manual rewrite source,
  destination hostname, and rule type; redeploy the static site after saving.
- **403 on controlled flow:** verify the frontend and backend are deployed from
  the same reviewed revision and the sample header survives the rewrite.
- **422 invalid sample:** redeploy both services; do not weaken the digest,
  filename, or media-type guard.
- **Provider/key error:** the wrong backend entrypoint or environment is active;
  disable the public demo and correct it before retrying.

## 21. Post-deploy evidence checklist

Record these facts in the DEPLOY-001 task record and Project Control Center:

- frontend public HTTPS URL;
- backend public HTTPS URL;
- exact deployed Git SHA;
- Render service names, types, region, and Free plan evidence;
- `/health` timestamp/status;
- arbitrary-upload 403 evidence;
- controlled PDF and DOCX end-to-end results;
- browser security-header results;
- provider credential absent/provider calls zero evidence;
- ephemeral-storage/cold-start constraints acknowledged;
- reviewer verdict/exact SHA and CI run URL/status;
- rollback/disable owner and current service state.

Use `NOT VERIFIED` for anything not checked. Never infer a live URL or successful
deployment from the Blueprint alone.

## 22. References

- [Render Blueprint specification](https://render.com/docs/blueprint-spec)
- [Render static-site headers](https://render.com/docs/static-site-headers)
- [Render redirects and rewrites](https://render.com/docs/redirects-rewrites)
- [Render free-tier limitations](https://render.com/docs/free)

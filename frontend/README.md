# AI IP Description Generator — Frontend

This directory contains the P0-005 local frontend MVP extended by P0-006 with
single-session draft editing, immutable revisions, section review records,
backend validation, and export of the selected validated revision.

The generated content is an AI-assisted draft for Human review. It is not legal
advice and is not filing-ready.

## Stack

- Next.js 16.3.6 with App Router
- React 19.3.0
- TypeScript 6.0.3 in strict mode
- ESLint 9.39.5 with the Next.js Core Web Vitals and TypeScript configurations
- Standard global CSS; no UI framework or client state library
- Playwright for synthetic offline browser tests (development dependency only)

## Local prerequisites

- Node.js 24 or another version supported by the locked Next.js release
- npm 11
- The repository Python 3.12 environment and FastAPI backend dependencies
- A local backend configured for the approved single-tenant orchestration API

Do not use confidential or unpublished research data until the unresolved
production authentication, storage, retention, and provider-data decisions have
been approved.

## Install

From `frontend/`:

```powershell
npm install
```

The committed `package-lock.json` is the dependency source of truth. Subsequent
clean installs can use `npm ci`.

## Backend expectation

Start FastAPI locally with orchestration explicitly enabled:

```powershell
$env:AI_IP_ENABLE_LOCAL_ORCHESTRATION_API="1"
```

The enablement flag is not authentication and is not a production security
boundary. The backend must expose upload, process, metadata, edited-draft
validation, and DOCX export.

The browser calls same-origin `/backend/*` paths. Next.js rewrites those requests
to the server-side `BACKEND_URL` value, which defaults to
`http://127.0.0.1:8000`. To set it explicitly before starting Next.js:

```powershell
$env:BACKEND_URL="http://127.0.0.1:8000"
```

`BACKEND_URL` is server-side configuration. No backend URL, API key, or secret is
exposed through a `NEXT_PUBLIC_*` variable.

## Development

```powershell
npm run dev
```

Open `http://localhost:3000`. The normal workflow consumes actual backend
responses; no analysis or draft fixture is embedded in production UI code.

## Quality checks and production build

```powershell
npm run lint
npm run build
npm run start
npm run test:e2e
```

The browser suite starts a synthetic-only FastAPI app with fake extraction/draft
runtimes and uses real local validation and DOCX rendering over HTTP. It needs
the repository Python environment and a Playwright Chromium install
(`npx playwright install chromium`). Build before the suite; the production
Next.js server uses port 3106 and the synthetic backend uses port 8000. The
build does not add or approve deployment configuration.

## P0-005 scope

Implemented:

- One-file PDF/DOCX upload with client UX checks and backend-authoritative validation
- Honest synchronous processing state without fabricated percentages or stages
- Human-readable canonical analysis, grounding labels, evidence, and locators
- Read-only patent description draft in canonical section order
- Dedicated missing-information, unresolved-conflict, author-question, and inference views
- Editable DOCX download through browser Blob handling with object URL cleanup
- Safe normalized API errors with correlation/reference ID display
- Responsive and keyboard-accessible application shell
- Session reset with no client persistence

Not implemented in the original P0-005 baseline:

- Authentication, authorization, login, accounts, or tenant isolation
- Database, persistence, job queue, polling, or WebSockets
- Draft editing, section approval, version history, comments, or collaboration
- Claims, patentability scoring, prior-art search, OCR, analytics, or deployment

## P0-006 local review boundary

- Only existing `PRESENT` abstract and paragraph prose is editable. Title,
  evidence, pointers, grounding labels, notices, drawings, IDs, and structure
  remain unchanged. Save creates a new immutable session revision; cancel
  leaves the prior revision unchanged.
- Per-section `UNREVIEWED`, `REVIEWED`, and `NEEDS_CHANGES` records live outside
  canonical AI-003 JSON. They do not identify an authenticated actor and are
  not audited or formal approvals. `NEEDS_CHANGES` never means approved.
- Backend validation checks schema, source-linked business rules, and abstract
  count. Deterministic checks cannot establish semantic entailment of newly
  edited prose; edited fields stay visibly flagged for Human source review.
  Evidence links and grounding labels are never upgraded by an edit.
- Export requires a validated saved revision and revalidates the exact payload
  server-side before rendering. `UNREVIEWED` does not block technically valid
  export. The DOCX remains a draft requiring specialist review.
- Edits, revisions, validation, and review status exist only in active browser
  memory. Reload, reset, or session loss discards all of them. There is no
  localStorage, IndexedDB, backend/database revision store, or durable audit.
- If processing had no selected title candidate, the title remains `MISSING`
  with `[AUTHOR CONFIRMATION REQUIRED]`. There is no post-analysis title
  selection or arbitrary title editing.

## Official brand asset

The header uses the Human-approved repository asset at:

`frontend/public/brand/vnuhcm-innovation-hub-logo.png`

Do not redraw, regenerate, replace, or download another version of this logo.

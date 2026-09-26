# AI IP Description Generator — Frontend

This directory contains the P0-005 local frontend MVP. It provides a read-only,
single-session workflow for uploading a PDF or DOCX, running the approved backend
pipeline, reviewing the canonical analysis and patent description draft, and
downloading an editable DOCX.

The generated content is an AI-assisted draft for Human review. It is not legal
advice and is not filing-ready.

## Stack

- Next.js 16.3.6 with App Router
- React 19.3.0
- TypeScript 6.0.3 in strict mode
- ESLint 9.39.5 with the Next.js Core Web Vitals and TypeScript configurations
- Standard global CSS; no UI framework or client state library

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
boundary. The backend must expose the approved local endpoints, including upload,
process, metadata, and DOCX export.

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
```

The build is a local production-mode compilation only. P0-005 does not add or
approve deployment configuration.

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

Not implemented:

- Authentication, authorization, login, accounts, or tenant isolation
- Database, persistence, job queue, polling, or WebSockets
- Draft editing, section approval, version history, comments, or collaboration
- Claims, patentability scoring, prior-art search, OCR, analytics, or deployment

Draft editing and versioned Human approval belong to P0-006, not this frontend
version.

## Official brand asset

The header uses the Human-approved repository asset at:

`frontend/public/brand/vnuhcm-innovation-hub-logo.png`

Do not redraw, regenerate, replace, or download another version of this logo.

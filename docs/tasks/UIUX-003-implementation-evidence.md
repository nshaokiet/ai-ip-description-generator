# UIUX-003 — Final visual polish and VIH brand alignment

| Metadata | Value |
| --- | --- |
| Version / date | 1.0.0 / 2026-10-11 Asia/Saigon |
| Author / owner | Codex / Human Product Owner |
| Workflow | V1; no V2 enrollment |
| Authorization | Human attachment “TASK: UIUX-003 — FINAL VISUAL POLISH & BRAND ALIGNMENT”, supplied in this task conversation on 2026-10-11 |
| Baseline main | `63d5a61235669ad7d32bb38d583789ea59ce5497` |
| Branch | `feat/uiux-003-final-visual-polish` |
| Status | Implementation candidate; exact-head CI and independent fixed-SHA review evidence are recorded in the single task PR |
| Required reviewer | Gemini 3.1 Pro High / Antigravity, STRICT READ-ONLY; verdict PENDING |

## Authorized presentation supersession

Human explicitly supersedes UIUX-001's Light/Dark/System selector and System default
with **always Light**, including saved dark/system values, OS changes and first paint.
UIUX-001 v0.1.0 and its approved history remain unchanged. This task is the scoped
presentation amendment: it does not change API/backend, upload limits, provenance,
Claims, revision/edit semantics, validation, v1 DOCX or public P2-006 availability.
Human authorizes local synthetic checks, affected tests, remediation, commit/push,
one PR and independent-review handoff; **merge/deployment are not authorized**.

| Old | New | Date | Author | Reason / decision | Breaking change |
| --- | --- | --- | --- | --- | --- |
| None | 1.0.0 | 2026-10-11 | Codex | Record Human UIUX-003 presentation supersession, implementation and verification | Intentional removal of theme UI only; no API/schema/template change |

## Implementation and quantitative evidence

- Deterministic server markup `data-theme="light"` and light CSS; remove prepaint
  storage/OS script, theme context/actions/read/write/subscriptions and dark CSS.
  Old `aiip.theme` remains harmless and untouched; only locale preferences are read
  or written. Locale failure fallback and workflow instance retention are preserved.
- Official logo bytes remain unchanged. Pillow RGB frequency sampling of the
  existing 5760×3241 PNG gives deep blue **#0252A4** (198,076 exact pixels), cyan
  **#1696D4** (228,811), orange **#F15F22** (60,962). These are observed samples,
  not a fabricated official brand manual. Blue dominates; cyan supports geometric
  outlines and orange is sparse. Approximate 70/20/10 is design guidance, not an
  asserted measured pixel ratio. Success/warning/error retain separate semantic colors.
- Logo display: desktop **190→166px (-12.63%)**; mobile **140→123px (-12.14%)**.
  Natural asset ratio is preserved with `height:auto`/`object-fit:contain`.
  Title: desktop **15.36→17.2032px (+12%)**, 390px mobile **12.48→13.9776px (+12%)**.
  Matrix assertions compare these actual computed values and require logo/divider/title
  centers to agree within 1px. Mobile title wraps; native locale control moves below.
- A local Segoe UI/Arial/Helvetica sans stack covers major UI and document preview;
  no web font/network dependency. Monospace IDs retain their diagnostic purpose.
  Heading line height leaves room for Vietnamese accents. Exported document fonts
  are unchanged. Native VI/EN select has explicit font weight, padding, label spacing,
  44px target, browser-native arrow and keyboard/screen-reader semantics.
- Five equal-height steps use centered content, shared horizontal padding, larger
  title/description text, 1px outer border/separators and rounded group corners.
  Current/completed/available/unavailable/processing/error/attention state calculation
  and permissions are unchanged in `WorkflowProgress.tsx`. Processing/error/attention
  retain explicit text/semantic colors. At 390px the five steps stack without scrolling;
  the tablet stepper retains its established accessible horizontal scroll.
- Original local SVG science (molecular bonds, network/flow/data geometry) and
  patent/engineering (document, leaders, gear, lightbulb, blueprint lines) artwork.
  Static, aria-hidden, noninteractive, reduced on tablet, hidden on mobile. Geometry
  tests keep both SVG bounds outside the central workflow at all nonmobile widths.
- Container borders #8295A9; control/editor/drop-zone borders #6B8195; focus #0252A4.
  Small draft section numbers use deep blue, avoiding cyan's insufficient 3.31:1
  contrast at small sizes. Actual text and control contrast reports are attached by tests.

## Verification mechanism

Working directory: repository `.worktrees/uiux-003-final-visual-polish`.
PowerShell via `functions.exec` → `exec_command`; normal sandbox escalation for
Git metadata/network dependency installation. Existing pinned `npm ci`, no manifest
or lockfile updates. No safety-status denial was encountered or bypassed.
Installed Next 16.3.6 bundled layout/CSS guides were read before editing.

```powershell
npm run lint --prefix frontend
npm run typecheck --prefix frontend
npm run build --prefix frontend
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
& '<repository>/.venv/Scripts/python.exe' -m pytest -q
# Start task-owned loopback servers, never a public deployment:
& '<repository>/.venv/Scripts/python.exe' -m uvicorn tests.e2e.offline_backend:app --host 127.0.0.1 --port 8000
# From frontend:
node node_modules/next/dist/bin/next start --hostname 127.0.0.1 --port 3120
# From task worktree:
$env:P1_005_EXTERNAL_SERVERS='1'
$env:PLAYWRIGHT_FRONTEND_PORT='3120'
$env:PLAYWRIGHT_BACKEND_PORT='8000'
$env:PLAYWRIGHT_PYTHON='<repository>/.venv/Scripts/python.exe'
npm run test:e2e --prefix frontend
```

The explicit Python override is necessary because the isolated worktree does not
have its own venv. Stop only the identified task server before rebuilding Next.
CI uses its established config-managed Ubuntu services and Python override.
Static demo: existing `RENDER_STATIC_EXPORT=1`, `NEXT_PUBLIC_DEMO_STAGING=1` build,
static secret-marker check, and `npm run test:e2e:demo --prefix frontend`.

## Test coverage and remediation history

`uiux-002.spec.ts` is renamed to `uiux-003.spec.ts`, preserving its 52 cases and
all locale/state/evidence/edit/dirty-dialog/validation/export/storage/privacy coverage.
The 30 theme matrix cases now verify light for 3 saved legacy preferences × 2
locales × 5 widths, with OS dark. Ten OS-light cases remain. Obsolete selector
interactions are replaced by fixed-light/first-paint assertions; no unrelated test
is deleted. The 25 integration and one performance cases remain. Integration and
two static-demo logo dimension assertions change to match the authorized 10–15% reduction;
the five existing demo workflow/restriction cases remain.

Initial focused checks: 12 PASS. Initial broad run: **72 PASS / 6 FAIL**, not accepted
as final evidence: one stale logo assertion, four DOCX inspection failures due to
omitted local `PLAYWRIGHT_PYTHON`, and one real mobile text-contrast defect. These were
resolved without backend changes. All six affected cases then PASS. A fresh final
comprehensive browser run and static-demo verification are recorded below/PR, not
inferred from the initial failed run. Python suite: **903 PASS / 3 SKIP**, one upstream
Starlette deprecation warning; Ubuntu CI's platform skips may differ.

## Final local results and visual inspection

Final comprehensive browser: **78 PASS / 0 FAIL / 0 SKIP / 0 FLAKY**, 139.7 seconds,
after the six affected cases passed their focused recheck. Lint, typecheck and normal
Next production build PASS. Python **903 PASS / 3 SKIP** (129.99 seconds). Static-demo
build and secret-marker scan PASS; final demo **5 PASS** (12.1 seconds). Its initial
3 PASS / 2 FAIL run exposed the two obsolete logo assertions; corrected with the same
proportional check and verified by the final five-case run, without runtime changes.
No repeat Python run is needed because no backend/test Python changes followed it.
Exact final-head GitHub CI remains required; a local result is not CI evidence.

Codex directly inspected actual 1440 VI/EN, 1920 desktop motif, 390 VI/EN, full desktop
review, readable review viewport, header and workflow close-ups. Observations: consistent
sans headings, complete Vietnamese diacritics, centered header/step content, readable
native locale, no stretched logo/obstructing art/body overflow. Mobile intentionally
uses a five-row workflow, increasing page height while exposing all five steps.
Reference-generated decoration images were not attached; original local SVG follows
the explicitly supplied composition and palette rather than claiming pixel identity.
See QA mapping for before and after files; machine-generated geometry/contrast is
separate from direct visual inspection. Neither is an independent reviewer PASS.

## AC reconciliation

These are implementer checks, not an independent verdict. Final SHA, exact-head CI,
artifact IDs and final readiness are authoritative in the published/read-back PR handoff.

| AC | Implementation / verification evidence |
| --- | --- |
| 01 | Theme control removed; matrix requires exactly one locale select and zero Appearance/Giao diện comboboxes |
| 02 | Server + CSS always light; stale light/dark/system, OS dark/light/change, JS-blocked first paint, denied/corrupt storage |
| 03 | One sans stack; measured fonts/no overflow; actual VI screenshots inspected for accent clipping |
| 04 | Native labeled locale select, improved typography/spacing; locale state/error/editor/revision/validation retention |
| 05 | Five steps use same computed sans typography; each remains present |
| 06 | Equal button heights, centered copy, consistent padding; measured matrix and workflow close-up |
| 07 | Sharper group/control/container borders; measured control boundary and focus contrast ≥3:1 |
| 08 | Computed logo reduction 12.63% desktop / 12.14% mobile, unchanged PNG bytes |
| 09 | Computed title increase 12%, logo/divider/title alignment, responsive wrapping |
| 10 | Original left molecule/network/flow/data SVG; inspected desktop screenshots |
| 11 | Original right document/gear/lightbulb/blueprint SVG; inspected desktop screenshots |
| 12 | Sampled logo blue/cyan/orange, sparse highlight, exact computed stroke checks, semantic status colors preserved |
| 13 | 390/768/1280/1440/1920 × VI/EN; no body/html overflow, safe margin bounds, five-step access, usable editing |
| 14 | Existing keyboard/modal/roving-focus/evidence behavior; 44px locale target, focus/nontext/text contrast, reduced motion |
| 15 | Unchanged backend/client/contracts/revisions/Claims/renderers; synthetic integration, Python, demo and safety regressions |
| 16 | Lint/typecheck/build/local regression; exact-head comprehensive CI required and linked in PR |
| 17 | [Real before/after provenance and capture mapping](../qa/uiux-003/README.md); Codex inspection, not Human visual acceptance |
| 18 | One implementation PR, final immutable SHA, CI/artifacts and strict read-only Gemini handoff; independent verdict PENDING |

## Limits and unresolved baseline dependency advisories

`npm ci` / read-only `npm audit` reports eight HIGH package entries in the **unchanged**
baseline: `next`, `sharp`, `source-map-js`, `eslint-config-next`, `@next/eslint-plugin-next`,
`fast-glob`, `micromatch`, `braces`. Entries include transitive duplicates, not eight
independent exploits. Runtime advisories include Next caching/Draft Mode/metadata/dev
MCP/image optimization, sharp's librsvg and indexed source-map denial of service;
lint's glob/brace chain also reports denial of service. No remediation, security
acceptance or exploitability PASS is claimed. This task adds no dependency and grants
no deployment; dependency remediation is outside its authorized visual scope and is
explicitly handed to the reviewer/Human for disposition. Never run automatic audit fix
or silently expand scope to resolve this report. No new secret/confidential source data
was introduced; dependency warnings are not represented as resolved findings.

Full WCAG/assistive-technology audit and cross-browser certification remain unverified.
Authentic supported-Claims positive E2E remains unverified; real figures are unauthorized;
Word pagination may differ; outputs remain drafts, not USPTO filing-ready. No paid
provider, real research, production/public deployment or subsequent task authorization.
MCP read returns **Unknown task: UIUX-003 — BLOCKED BY TOOL CAPABILITY**; no fabricated
claim/lease/state. Google Drive synchronization is unverified. Independent Gemini
review/merge/closeout remain pending and are not authorized by implementation readiness.

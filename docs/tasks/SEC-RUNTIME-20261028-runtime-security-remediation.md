# SEC-RUNTIME-20261028 — Runtime and CA security remediation

| Field | Value |
| --- | --- |
| Version / previous | 0.1.0 / none |
| Date / owner | 2026-10-28 / Codex |
| Human authorization | SEC-RUNTIME-20261028 MINIMAL SECURITY REMEDIATION: implementation, local tests, isolated branch and publication; no merge or deploy |
| Status | IMPLEMENTED_CANDIDATE — independent exact-SHA review and required hosted CI PENDING |
| Base | `53c253be874236c6f38a5333a6f7f3390de9f51e` |
| Review | Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY, pending on final GitHub SHA |
| Breaking change | Node engine support intentionally narrows to patched Node 24 (`>=24.22.1 <25`); npm engine checks can be warnings unless strict enforcement is enabled. No application/API contract change. |

## Advisory and risk

The [Node October 2026 security advisory](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases) describes high-severity DNS, TLS and Brotli flaws including CVE-2026-105482, CVE-2026-105483, CVE-2026-106069 and CVE-2026-111497. The [Render eMudhra advisory](https://render.com/docs/advisory-emudhra) requires patched trust stores and recommends Certifi 2026.10.19 or later. CI previously explicitly selected Node 24.18.0 in both jobs. Affected code paths and actual live exposure depend on use; the running Render environment, service version, trust configuration and outbound traffic remain NOT_VERIFIED. No claim of exploitation or live safety is made. `npm audit` does not establish the security of the Node executable.

## Scoped change

- Both existing `actions/setup-node@v7` pins become `24.22.1`; all jobs, conditions, mandatory security uploads and other workflow semantics are unchanged.
- `render.yaml` specifies `NODE_VERSION=24.22.1` for the static frontend build. This does not change a live service. [Render Node version precedence](https://render.com/docs/node-version) places a service Dashboard `NODE_VERSION` above `.node-version` and package engines; live overrides must be verified before deployment. No second `.node-version` pin is introduced.
- Backend requirements add exact `certifi==2026.10.19`, matching existing exact pins. The official [PyPI release metadata](https://pypi.org/pypi/certifi/2026.10.19/json) identifies wheel SHA-256 `42d35340cc5b9ba78e818ddbff0c5b1c2b779de448a340fd1b989f5fa8670e1b`; the downloaded wheel was independently hashed and installed to an isolated temporary target using `--no-index --no-deps`. This is not a fully hash-locked Python dependency graph.
- Frontend, its local glob adapter, and MCP package engines become `>=24.22.1 <25`; matching lockfile metadata is updated. Comparison after normalizing these metadata fields proves no package graph, version or integrity changes. npm `engines` alone is advisory under non-strict npm configuration; verify actual Node version at execution.
- `tests/test_sec_runtime_20261028.py` covers CI/Render settings, engine/lock metadata, Certifi requirement and TLS verification. Its installed-bundle check is opt-in (`SEC_RUNTIME_REQUIRE_PATCHED_CERTIFI=1`) and was executed against the isolated patched target; ordinary default execution skips that check explicitly.

## Validation and limitations

On Node 24.22.1: frontend offline install, lint, typecheck and build passed; frontend security suite 73/73 passed. MCP offline install, typecheck/build and 152/152 tests passed. npm installs first ran under installed Node 24.18.0 and produced expected engine warnings; all stated compatibility tests were rerun with 24.22.1. Provider tripwire/demo tests passed 12/12 using isolated Certifi 2026.10.19; `pip check` passed with the isolated target. Runtime tests passed 7/7 with the installed-bundle check enabled. A loopback TLS connection rejected a self-signed certificate with the patched Certifi bundle. An earlier same test used local Certifi 2026.7.22 before the patched-target path was set; it was repeated successfully with 2026.10.19. Workflow and Render YAML parse and semantic comparison passed; actionlint was not available. No paid provider, confidential paper or hosted CI was used.

The assessment report at `D:/AIIP-RESTART-20261028/security-runtime/SEC-RUNTIME-20261028-RENDER-ADVISORY-ASSESSMENT-AND-SPEC.md` has observed SHA-256 `ecb30fc928a2a42834c674aa9187e75046ec9ebdaa9bad6ce584d28a4f52db4e`; independent historical checksum NOT_VERIFIED. The report's inference about live Render exposure or urgency is not treated as live evidence.

## Dependencies and release gates

PR #147 separately updates Next/Zod and retains its independent review at `c50be576b39acd2eac9da096efd11060545463d1`; this candidate starts from current main and does not contain its patch. Both touch frontend package files; reconcile non-destructively on the actual future base and re-review/retest any changed final SHA. PR #144 separately changes the same workflow; reconcile after its actual disposition and preserve mandatory evidence. PR #146 remains a separate specification review/CI flow. Existing reviewed SHAs are not altered.

Hosted CI and artifact storage recovery remain unverified/blocking. No PR is opened while its pull_request trigger would start a known-blocked workflow. Before any future merge verify current scope, exact-head independent review, required hosted CI, repository protection and actual Render auto-deploy/preview settings; Blueprint declares `checksPass` and current live settings are NOT_VERIFIED. Render environment changes, deployment/redeployment and budget changes require separate Human authorization. After separately authorized deployment, verify actual build/runtime Node, Certifi and CA configuration with appropriate service-level evidence.

Rollback any later accepted merge via a separately reviewed normal revert appropriate to its actual merge method, without history rewrite. A revert restores vulnerable/unpinned runtimes and creates an active security blocker; assess safe service suspension or another Human-authorized mitigation before deployment decisions.

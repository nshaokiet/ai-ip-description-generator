# UIUX-003 synthetic visual QA

Version 1.1.0, 2026-10-12, Codex. Only synthetic fixtures; no real research.

## Before provenance

The seven PNGs in `before/` are unchanged bytes extracted from the actual UIUX-002
[CI run 38109920594](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/38109920594),
artifact `11690887817`, `uiux-002-synthetic-browser-qa`. Its immutable implementation
head is `af5406669fcb53593184461ba0dab0c7b1ba67e4`. Artifact ZIP digest:
`sha256:01f203ddc82984a18850fbad046e98e5d9c6ff20d4139afbf9e5bdd81dc30fe5`.
The implementation tree is preserved by UIUX-002 merge `e6a47c900d227e2c028156e0dad5225d721e3353`;
UIUX-003 main baseline `63d5a61235669ad7d32bb38d583789ea59ce5497` adds factual documentation only.
Artifact metadata and available local ZIP were checked; images are not recreated
approximations. The earlier CI was Ubuntu Chromium; local after images are Windows
Chromium, so compare layout and measured CSS geometry, not identical font rasterization.
UIUX-003's CI supplies Ubuntu after images for the same platform comparison.

| Before file | Corresponding after file in `frontend/test-results/` |
| --- | --- |
| [1440 VI](before/home-1440-light-vi.png) | `uiux-003-presentation-1440-light-vi/home-1440-light-vi.png` |
| [1440 EN](before/home-1440-light-en.png) | `uiux-003-presentation-1440-light-en/home-1440-light-en.png` |
| [1920 VI](before/home-1920-light-vi.png) | `uiux-003-presentation-1920-light-vi/home-1920-light-vi.png` |
| [1920 EN](before/home-1920-light-en.png) | `uiux-003-presentation-1920-light-en/home-1920-light-en.png` |
| [390 VI](before/home-390-light-vi.png) | `uiux-003-presentation-390-light-vi/home-390-light-vi.png` |
| [390 EN](before/home-390-light-en.png) | `uiux-003-presentation-390-light-en/home-390-light-en.png` |
| [1440 review EN](before/review-1440-light-en.png) | `uiux-003-review-edit-guard-evidence-and-export-1440/review-1440-light-en.png` |

Header and workflow close-ups are `header-closeup.png` and `workflow-closeup.png`
under `uiux-003-presentation-1440-light-vi/`. A readable desktop review capture is
`review-workspace-viewport.png` under the 1440 review case. The full-page review
image preserves the complete draft and evidence; the viewport is an additional capture.

## Reproduction and evidence access

From the task worktree run the normal frontend lint/typecheck/build and Playwright
commands in the [implementation ledger](../../tasks/UIUX-003-implementation-evidence.md).
`uiux-003.spec.ts` captures actual browser screenshots, layout measurement JSON,
text/nontext contrast reports and first-paint/light-state assertions. Filenames
containing `dark` or `system` identify the **saved legacy preference under test**;
all UIUX-003 screenshots must render light.

The single UIUX-003 PR handoff records final implementation SHA, exact-head CI run
and `uiux-003-synthetic-browser-qa` artifact ID/URL. CI archives both these baseline
files and the fresh browser output before static-demo tests overwrite `test-results`.
Artifacts expire after seven days; download them for extended independent review.
Tracked baseline images remain available in Git. No generated output containing
real paper data is committed.

Codex visual inspection is implementation self-QA, not Human acceptance or an
independent Gemini verdict. Full WCAG/assistive-technology certification is not claimed.

## Integration QA — 1.0.0 → 1.1.0 (12/10/2026)

Human-authorized main integration preserves all seven original before PNGs and every UI/test source byte. New baseline is DEP merge `81942a249f164859a9687e77abfed12e90bfb197`; original UIUX reviewed source remains `102b7e90dc3bfc1f79c197a20184f97b89070bf2`, historical PASS only. Fresh integrated 78-case browser output is copied to ignored `tmp/uiux-003-integration/local-after/` before static-demo cleanup; screenshot mappings above remain unchanged. [Actual local integration/security/regression evidence](integration-validation.json) includes five directly inspected views and the resolved local Temp failure. New exact-head CI archives `uiux-003-synthetic-browser-qa` before demo cleanup, including all tracked before images; actual run/artifact references are recorded in PR #104 handoff. No independent verdict or merge is implied. Breaking change: No — evidence/provenance update only.

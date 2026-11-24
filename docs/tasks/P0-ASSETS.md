# P0-ASSETS — bounded DOCX embedded-image provenance foundation

| Field | Value |
|---|---|
| Version / date |0.1.0 /22/11/2026 Asia/Saigon |
| Authority | Actual Human NEXT DEVELOPMENT EXECUTION Phase3, current22/11 conversation; task-specific V1 scope |
| Owner / implementer | Nguyễn Song Hào Kiệt — Independent Developer /Codex |
| Base / branch | main6bb947c1cf67bcfb3ffc935b3a3fafcafb87f0af /feature/p0-assets-docx-foundation-20261122 |
| Status | IMPLEMENTED_CANDIDATE /OFFLINE_VERIFIED_DOCX_SUBSET /INTEGRATION_PENDING /REVIEW_PENDING |
| Scope | Native registered DOCX PNG/JPEG byte extraction plus source/part/relationship/XML-paragraph locators, caption/text-reference candidates and existing parsed-table provenance |
| Boundary | No image decode/render/redraw, no PDF image extraction, no provider/browser/deploy/real paper, no unmerged169/170/171 dependency |
| Reuse | Existing upload validator/storage/registry/preparation/normalization; existing source hash and immutable native data, no new dependency or search/ingestion pipeline |
| Risk | HIGH data/path/ZIP/asset misassociation; actual final-SHA independent Security AND Quality required |

Before-code contract: explicit trusted-host inspection authorization bound to owner/actor/context/document/source hash; original registered bytes rechecked before/after processing. PNG/JPEG retained byte-identical under32 assets/4MiB each/16MiB total, no decoding or filesystem extraction. XML2MiB bounds/no DTD/entities; existing package validator still applies. No asset content/text in default repr/errors/logging.

Manifest source SHA, original media member and SHA256, relationship IDs and XML paragraph positions are factual locators. DOCX source page and related specification section remain unknown; captions and in-text figure references are candidates, never guessed associations. All asset fidelity/redraw statuses REVIEW_REQUIRED. Unsupported PDF/legacy/other formats are explicitly flagged rather than claimed supported. Existing parser supplies TABLE identities/hashes; no duplicate table parser.

AC/tests: actual synthetic DOCX upload with embedded image/table/caption/reference → byte-identical image hash/source binding and deterministic locators; safe bounds/unsafe relationship/member/DTD rejection; authority/source-mutation/TTL/stale registry denial; immutable outputs/no decode/no SDK/network. No output/runtime integration claimed. No overall P0-ASSETS/FIG completion until broader supported formats/fidelity/reviews/integration gates.

Changelog new0.1.0,22/11/2026,Codex: minimum scoped DOCX asset contract recorded before implementation; no existing API/policy breaking change.

## Actual evidence and remaining scope

Final local51PASS/0FAIL/0SKIP,3.45s:18 new asset cases +26 existing parser +7 provider-tripwire regressions,1 existing deprecation warning. Actual synthetic DOCX upload with PNG/JPEG/table/caption/body reference proves byte/hash preservation and deterministic locators, actor/context/source binding, immutable metadata, no Image.open/SDK/network and denial of source mutation/expiry/authority/bounds/DTD/UTF16/external image relationships. Default repr hides raw image and caption text. PDF/other formats produce explicit unsupported/review flags; they are not falsely counted as extracted.

Native source inspection requires host-authenticated ownership/actor/context; registry has no team RBAC and this helper adds none. The inspection action/hash and actual UTC timestamp are metadata, not authenticated Human identity. No persistent audit/retention policy or browser/file delivery is added. Source/bytes captured does not mean decoded image/pixel fidelity or caption/specification association verified. Both related section and DOCX page remain None. No automated redraw is implemented.

## Section20 handoff

```text
Task ID: P0-ASSETS
Agent: Codex
Reviewer: actual Gemini4 Argon(High) independent Security AND Quality requested; NOT_RUN
Status: IMPLEMENTED_CANDIDATE /OFFLINE_VERIFIED_DOCX_SUBSET /INTEGRATION_PENDING /REVIEW_PENDING
Version: task0.1.0 /native manifest1.0.0
Work completed: bounded DOCX embedded PNG/JPEG byte/provenance capture; caption/text-reference candidates; existing parsed-table locators; explicit unsupported states
Files affected: document_assets.py, test_document_assets.py, P0-ASSETS.md, README.md, Control Center
Evidence checked: main6bb947c, actual uploaded synthetic images/documents,51 local tests, byte hashes/source/XML/member/authority/TTL/tripwire negatives
Findings: PDF image extraction, image decoding/fidelity, caption/page/spec association and redraw NOT_IMPLEMENTED or REVIEW_REQUIRED
Decisions: retain raw source bytes; no inference of scientific structure; no new dependency or unmerged-code integration
Issues: exact-head CI/security, genuine independent reviews and applicable integration gates remain
Security impact: no decode/ZIP filesystem extraction/provider/network/browser/public route/real paper/deploy
Recommended next action: final-SHA independent review; accepted security/bridge/consumer contracts; separately scoped broader asset support and fidelity validation
```

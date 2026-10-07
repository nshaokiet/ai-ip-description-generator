# Quality Reviewer Agent Contract

Contract version: 0.1.0
Role ID: `QUALITY_REVIEWER`
Review type: `QUALITY`
Workflow V2 status: NOT ACTIVATED

## Purpose

The Quality Reviewer independently reviews the exact final implementation SHA for
specification compliance, correctness, architecture, regression, compatibility,
test adequacy, API/schema behavior, failure handling, maintainability, and scope
discipline. Its authority is limited to the Quality review stream.

For R3 AI/conversion work, review additionally covers source fidelity, evidence
preservation, invention boundaries, prior-art versus inventor-contribution
separation, unsupported inference, technical relationships, terminology,
missing-information behavior, and end-to-end traceability.

## Independence and authority

- Review the frozen spec, exact base SHA, exact final implementation SHA, diff/file
  set, and relevant tests/CI/evidence.
- Author the Quality verdict independently from the Security verdict.
- Do not wait for or consume the Security verdict as a basis for the Quality
  conclusion.
- Do not modify tracked implementation or remediate code while acting as reviewer.
- A review that modified tracked implementation cannot satisfy an independent PASS;
  implementation must be cleaned/remediated by the Implementer and re-reviewed.
- A changed implementation SHA invalidates applicability of the prior PASS.

Compatible existing B2/B3 capabilities include `project.get_state`,
`project.get_assignments`, `project.get_spec`, `review.start`, `review.submit`,
`review.get_status`, and `project.get_merge_gate`. `review.submit` is operational
state for the durable review artefact; it does not independently verify Git/CI or
Human provenance.

## Forbidden actions

- Modify tracked implementation while serving as Quality Reviewer.
- Act as Implementer for the same review evidence stream.
- Submit a Security verdict under Quality authority.
- Convert recorded claims into authoritative verification without the designated
  verifier/source contract.
- Treat `provisional_ready` as authoritative merge eligibility.
- Expand its own authority, activate Workflow V2, or waive Human stop conditions.

## Required artefact

Use `../review-templates/quality-review.md` as the durable review format. Record
the exact identities and evidence required by the GOV-AGENT-001 review artefact
model, including `tracked implementation files modified`.

`RECORDED != VERIFIED` and `provisional_ready != authoritative_merge_eligible`.

# Workflow V2 synthetic lifecycle pilot 01

This is a synthetic, non-production governance exercise for
`GOV-AGENT-001-F-PILOT-01`. Its frozen specification is v0.1.0 at
`fcb52eb30da03df4d1ce6bc7487bc58f7135014f`.
The activation/base commit is `9c291325d409f74bc767f9b870e81d75c9b70802`.

## Synthetic record

```json
{
  "pilot_id": "GOV-AGENT-001-F-PILOT-01",
  "workflow_version": 2,
  "activation_commit": "9c291325d409f74bc767f9b870e81d75c9b70802",
  "spec_version": "0.1.0",
  "synthetic_value": 7,
  "expected_value": 15,
  "security_review_required": true,
  "quality_review_required": true,
  "rule": "result = input * 2 + 1",
  "cases": [
    {"input": 7, "expected_value": 15, "computed_value": 15}
  ]
}
```

## Lifecycle and evidence boundaries

Candidate A contains 7→15. The predefined candidate B adds 11→23 without
changing the frozen specification or the first case. The focused test accepts
only these two stages; final B acceptance requires both cases.

The real drill uses B1 role/spec/lease capabilities, B2 immutable implementation,
CI and review evidence, and B3 persisted candidate CAS and fail-closed merge gates.
Operational evidence is retained outside the implementation branch, with real
source references and hashes. This document and its tests cannot authenticate
Human authority, reviewer identity, enrollment, CI or merge.

Required observations are: actual A CI followed by B pointer selection; rejected
CAS rollback and winning retry idempotency; A evidence retained as stale;
checkpoint/read/resume preserving V2 history; fresh B CI; and separate read-only
Security and Quality reviews on the same final SHA. No independent verdict is
supplied by this artifact or its Implementer.

`RECORDED != VERIFIED` and
`provisional_ready != authoritative_merge_eligible`.
Authoritative adapters remain unavailable; merge requires the Phase E
MANUAL_EXTERNAL procedure against real sources after both independent reviews.
The pilot remains incomplete until those reviews, merge and post-merge
verification succeed. Automatic R0–R4 routing is NOT ACTIVATED; Phase G is
NOT STARTED. No product, provider, research data or production work is authorized.

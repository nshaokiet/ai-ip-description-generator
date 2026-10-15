# AI-CONV-003 synthetic Claims authority fixtures

`v1.0.0/candidate-semantics.json` contains identifiers for the preliminary
METHOD/PROCESS and COMPOSITION models used by the offline tests. The file is
synthetic, carries no authenticated Human identity, and is not a released
P2-002 through P2-006 input.

Runtime-bound evidence, decisions, assertions and canonical digests are built
inside `tests/backend/test_synthetic_claims_authority_v1.py` so every test can
bind them to the exact source document, evidence snapshot, session and revision
under test. The fixture must never be interpreted as a positive METHOD,
PROCESS or COMPOSITION Claims authorization.

# Ai Security

- name: `ai-security`
- version: `1.0.0`
- role_scope: `SECURITY`

Governance takes precedence over this skill. A task specification may narrow its behavior but may not expand authority.

## Purpose

Review AI/provider/prompt/file-ingestion security and confidential-IP boundaries independently.

## Applies when

Security review when AI conversion, prompts, uploaded documents, providers, model runtime, or confidential research are in scope.

## Required inputs

- exact review SHA/diff
- data-flow/provider configuration
- prompt/instruction boundaries
- file-ingestion/parser behavior
- authorization for real/confidential data if any

## Allowed actions

- review prompt injection and instruction/data separation
- review secret/provider/data handling and logging
- review malformed file/resource exhaustion and outbound/network risks

## Forbidden actions

- send research data to unapproved providers
- expose secrets or full confidential source text in review artefacts
- authorize provider/model/data use
- modify remediation code

## Procedure

1. Identify AI/data/provider trust boundaries and authorized data classes.
2. Test/inspect instruction-data separation, file handling, secret/logging, network/provider behavior.
3. Evaluate prompt injection, parser/resource exhaustion, exfiltration, and confidentiality controls.
4. Record exact evidence and security verdict.

## Required checks

- no unauthorized provider/data path
- secrets/logging boundaries are safe
- research content cannot redefine agent authority
- file/parser abuse controls are addressed where applicable

## Output contract

AI-security findings and SECURITY verdict bound to exact SHA with confidentiality-safe evidence.

## Failure conditions

- confidential-data authorization is unclear
- provider/network behavior exceeds authorization
- required security evidence is unavailable

## Handoff

Block the affected gate and route policy/authorization decisions to Human; remediation remains Implementer-owned.

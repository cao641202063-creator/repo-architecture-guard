## Why

As repositories grow, reading every file is slow and still fails to reveal the
end-to-end logic or documentation consequences of a change. A single agent's
self-review also has predictable blind spots before human approval.

## What Changes

- Add a scope-first, evidence-based global-logic navigation workflow built on
  the existing code map rather than broad repository rereading.
- Require a documented impact analysis for product, user, API, operational,
  and technical documents after every code change, and update the documents
  that are affected.
- Add a bounded independent-agent audit loop for full-track changes: an auditor
  reviews the completed change, the primary agent makes one evidence-based
  revision pass, then a human receives the final audit disposition.
- Add a capability-specific reference contract and package tests that prevent
  the new rules from drifting across the Skill and generated policy.

## Capabilities

### New Capabilities

- `scale-aware-delivery-audit`: Efficient global-code understanding,
  documentation impact analysis, and independent-agent delivery audit.

### Modified Capabilities

- None.

## Impact

The canonical Skill, generated AGENTS policy, code-map and artifact contracts,
README, product goal, test suite, and delivery documentation will change. The
workflow uses delegation only when the environment provides it and adds no
runtime dependency.

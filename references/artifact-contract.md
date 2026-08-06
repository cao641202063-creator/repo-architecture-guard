# Product and Delivery Artifact Contract

Use project-defined equivalent paths when `AGENTS.md` maps them explicitly. Keep human-facing artifacts in 简体中文 unless project policy says otherwise.

## Persistent Product Context

Maintain these only when relevant:

- `ProjectGoal.md`: target users, outcome, milestone, success criteria, non-goals, constraints, and approved product decisions.
- `docs/ai/project-status.md`: evidence-backed capability, implementation, test, documentation, risk, and next-decision status.
- `docs/ai/code-map.json` and `code-map.md`: navigation facts, not a substitute for source reading.

Record unknowns as decisions needed. Do not rewrite product goals to reflect implementation detail.

## System of Record

Each material change has one owner:

- Trellis task for long personal or small-team delivery;
- OpenSpec change for formal, shared, or multi-repository specification;
- project-native equivalent if explicitly configured.

Link other artifacts to that owner. Do not duplicate a PRD, design, task list, or decision log.

## Conditional Review Artifacts

Create `docs/reviews/<change>-solution-review.html` only when the selected risk policy requires review: L2/L3 changes that alter a user flow, material product rule, permission boundary, or non-UI state/data flow. It records goal, roles, scope/non-goals, proposed flow, rules, assumptions, decisions, version, and approval status.

Create `docs/reviews/<change>-test-cases.html` only for L2/L3 user-facing work or explicit product review. It maps meaningful scenarios to unit, integration, contract, browser, or manual verification. It is not a substitute for executable tests.

## Verification Evidence

Use the selected risk level:

- L0: relevant lint, format, or build evidence.
- L1: `test:changed` and applicable lint/type-check.
- L2: L1 plus relevant contract/integration and one final smoke pass.
- L3: L2 plus one final full regression.

During coding, retain focused evidence. After all repairs, run the chosen broader suite once on the final candidate. Do not create repeated full-suite evidence for intermediate edits.

When final artifact validation is required, record source revision/dirty state, build command and time, artifact or environment identity, and test commands/times. Never associate tests with a different revision or build.

## Documentation Impact

After code changes, classify relevant product, user, API/contract, operational, technical, test, and navigation documents as updated, unchanged with evidence, superseded, obsolete, or requiring decision. Update affected documents and project status. Do not create a separate report merely to repeat unchanged content.

## Independent Audit

Perform independent read-only audit only for L3, release-candidate L2, or an explicit request. Give the auditor the request, owner artifact, Context Brief, final diff, documentation impact, and verification evidence. Record scope, findings, disposition, revisions, and residual risk. If no independent facility is available, disclose self-review instead.

# Human-Review HTML Contract

Create self-contained or project-runnable HTML only when the selected delivery gate requires a human-review artifact. Write human-facing content in 简体中文 unless project policy says otherwise.

## Solution Review

For L2/L3 changes that alter user flow, product rules, permissions, or material state/data flow, store `docs/reviews/<change>-solution-review.html`.

Include the goal, affected users and roles, scope/non-goals, assumptions, unresolved decisions, version, approval status, proposed flow, business rules, and relevant state/data/permission diagram. UI reviews also cover screens, navigation, actions, validation, normal/empty/loading/error/permission states, responsive behavior, and accessibility expectations.

Do not create this artifact for L0/L1 changes unless a reviewer requests it.

## User-Scenario Matrix

For L2/L3 user-facing work or explicit review, store `docs/reviews/<change>-test-cases.html`. Include scenario ID, requirement/outcome, role, setup, steps, expected result, category, priority/risk, automation target, and review status.

Cover meaningful golden, alternative, boundary, error/recovery, permission, persistence, compatibility, responsive, and accessibility risk. Show intentional exclusions. Do not enumerate equivalent permutations.

## Final Report

When final artifact validation or product-facing acceptance applies, store `artifacts/test-reports/<change>-report.html`. Lead with delivered outcome, scenario conclusion, failures/blocks, and user impact; include screenshots only when they prove a material state or flow. Then record exact build provenance, documentation impact, audit/self-review status, and supporting commands/logs.

L0/L1 work may report the same evidence in the final handoff without an HTML report.

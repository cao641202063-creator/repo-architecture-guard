---
name: repo-architecture-guard
description: Route code changes from verified product and repository context. Use before source, test, API, schema, configuration, build, refactor, bug-fix, or user-facing implementation work in an existing repository to assess impact and risk, reuse architecture, choose the minimum sufficient workflow and verification, and coordinate Grill-me, Trellis, OpenSpec, or Superpowers only when needed.
---

# Repository Architecture Guard

## Role

Act as the single entry point for delivery work. Establish product and repository facts, classify risk, then invoke only the capabilities that reduce uncertainty. Do not make a second PRD, plan, or test policy when an existing project artifact owns it.

Project `AGENTS.md`, explicit product-owner decisions, and project-required checks override this skill.

## Context Gate

Before editing:

1. Read the nearest `AGENTS.md`, `ProjectGoal.md`, current status, and relevant active specification.
2. Run `code_map.py check --root <project-root> --json`. Bootstrap or update only when missing or stale.
3. Follow relevant map nodes into the owner, callers, contracts, tests, and documents. Read source before changing it.
4. Search for reusable components, services, contracts, fixtures, and project commands.
5. State a concise Context Brief: user value, affected roles, scope/non-goals, evidence inspected, impact slice, reusable capability, unresolved decisions, selected risk level, workflow, and verification plan.

Classify gaps as **blocking question**, **owner decision**, or **reversible assumption**. Stop only for a material conflict or missing decision; record reversible assumptions and continue.

## Route Workflows

Use one system of record for each change.

| Need | Route |
|---|---|
| Requirement or design remains ambiguous | Invoke `$grill-me` first. Ask one decision at a time, research repository facts before asking, then save the agreed decisions in the selected system of record. |
| Personal or small-team work spans sessions | Use Trellis as the task, memory, and handoff system. Do not also create a parallel OpenSpec proposal. |
| Multi-repo, formal, reviewable, or shared requirement | Use OpenSpec as the specification system of record. Reconcile existing changes; do not create a Trellis PRD copy. |
| TDD, debugging, plan review, or completion evidence is needed | Invoke only the matching Superpowers skill: `$test-driven-development`, `$systematic-debugging`, `$writing-plans`, or `$verification-before-completion`. Do not invoke the complete Superpowers workflow by default. |
| Narrow, clear, local work | Stay in this skill's lightweight path; do not invoke another workflow. |

For an active Trellis or OpenSpec change, update the owner artifact instead of duplicating decisions elsewhere.

## Risk and Validation Policy

Classify before coding. Use the highest applicable level.

| Level | Trigger | Required verification |
|---|---|---|
| L0 | Documentation, copy, mechanical edit, isolated style change | Relevant lint, format, or build check. |
| L1 | One module, narrow bug fix/refactor/configuration; no public contract or material behavior change | `test:changed` plus applicable lint/type-check. |
| L2 | Cross-module behavior, UI flow, state/persistence, API/event contract, shared component, or substantial refactor | `test:changed` + relevant integration/contract check + `test:smoke` once after implementation is complete. |
| L3 | Permission/security boundary, payment, data migration, shared infrastructure, critical business path, or project-mandated release gate | L2 checks + `test:full` once on the final candidate; perform independent audit when available. |

Use project-native commands. Prefer this interface when the project defines it:

```text
test:changed     affected unit tests
test:contract    API, event, schema, or integration contract tests
test:smoke       critical user-path checks
test:full        complete regression
```

Never run a full suite after each edit. During implementation rerun only the focused failing or affected check. Run broader checks once after all intended changes and repairs are complete. A failing required check requires diagnosis, a reproducing test where applicable, repair, and a rerun of the required scope.

## Delivery Gates

- Use TDD for changed behavior. For a bug, first create the smallest test that demonstrates the defect.
- Create an HTML solution review only for L2/L3 changes that alter a user flow, product rule, permission model, or material non-UI state/data flow. Skip it for L0/L1 unless requested.
- Create the HTML scenario matrix only for L2/L3 user-facing work, or when a product owner asks for review.
- For UI work, use project-native browser tests and meaningful screenshots only when they verify a material state or flow.
- Build and test the exact final artifact once before delivery when L2/L3 or project policy requires it. Do not repeatedly rebuild unchanged candidate states.
- Run an independent read-only audit only for L3, release-candidate L2, or when explicitly requested. Otherwise perform and disclose self-review.

## Architecture and Documentation

Extend the current owner rather than creating parallel implementations. Change the code map only when ownership, public symbols, dependencies, routes, data boundaries, reusable components, or test relationships change.

After code changes, assess product, user, contract, operational, technical, test, and navigation documentation. Update affected documents; for unchanged relevant documents, record concise evidence. Update project status with verified outcomes and remaining risk.

## Completion

Before handoff, invoke `$verification-before-completion` when available and report:

- delivered outcome and affected scope
- architecture reused or changed
- selected risk level and why
- commands actually run and their results
- whether final-build, review, and audit gates ran or were intentionally not required
- documentation/code-map updates
- residual risks, skipped checks, and external blockers

Never claim a skipped check passed.

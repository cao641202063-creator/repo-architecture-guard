---
name: repo-architecture-guard
description: Use before every code change to align work with ProjectGoal.md, inspect current project status and a maintained code map, reuse existing architecture, select lightweight or full OpenSpec/Superpowers delivery gates, require TDD and user-scenario verification, test the latest build, and update documentation. Trigger for source, test, API, schema, build, configuration, refactor, bug-fix, and user-facing implementation tasks in existing repositories.
---

# Repository Architecture Guard

## Purpose

Make code changes from verified product and repository context instead of
starting from the request alone. Keep the code map compact, treat source as the
truth, and finish with evidence from the exact build being delivered.

Project `AGENTS.md` instructions and explicit user decisions override defaults
in this skill.

## 语言

除非产品负责人或项目规则另有要求，所有面向人类的提问、Context Brief、方案确认、
测试场景、报告、文档影响分析、审计结论和最终交付说明均以简体中文为主。命令、路径、
文件名、代码、API 标识符、配置键、JSON 字段及机器可读协议保持原文，确保可复制和
可执行。无需仅为语言策略重写未受当前变更影响的历史证据。

## Requirement Readiness and Product Challenge

Before selecting a delivery track or planning implementation, assess whether
the request states the user value, affected users, scope and exclusions,
acceptance criteria, business or data rules, permissions or failure behavior,
constraints, and priority where relevant. Compare it with explicit product
decisions, goals, approved designs, and repository evidence.

Classify gaps explicitly:

- **blocking question**: a missing fact or conflict would materially change
  scope, behavior, acceptance, risk, or implementation; ask focused questions
  and wait before implementation.
- **decision needed**: the product owner must choose among meaningful options;
  explain the trade-off and recommend an option.
- **reversible assumption**: the detail does not materially change behavior or
  risk; record it for review and continue only if no blocking question remains.

Challenge a request when it names a solution without the user problem or
success measure, conflicts with an approved decision or non-goal, has an
unverifiable acceptance criterion, or omits a material boundary. Do not invent
business behavior merely to make the request implementable.

## Required References

Load only the reference needed for the current gate:

- Project policy prompt: `references/agents-template.md`
- Product and delivery assets: `references/artifact-contract.md`
- Map nodes and operations: `references/code-map-contract.md`
- Human-review HTML: `references/html-review-contract.md`

## Initialize a Project

For a new or previously unmanaged project, use the standard-library initializer
relative to this `SKILL.md`:

```text
python <skill-directory>/scripts/init_project.py --root <project-root>
```

The command collects product input, creates missing product goal and status
files, safely adds or replaces the marked policy block in `AGENTS.md`, and
bootstraps or updates the code map.

Use `--brief <path>` to retain an existing UTF-8 business brief as evidence.
Use non-interactive product flags for automation. Existing goal and status
files are preserved unless the user explicitly supplies `--force-goal` or
`--force-status`. Use `--no-code-map` only when the user intentionally requests
documentation-only initialization.

After initialization, review unknown fields with the product owner. The
initializer structures supplied evidence; it does not approve product
assumptions.

## Trigger

Run this skill before modifying:

- production or test source
- API, event, database, or file contracts
- application configuration or feature flags
- build, packaging, deployment, or CI behavior
- shared UI components, styles, or interaction patterns
- architecture, module boundaries, or reusable methods

Documentation-only analysis does not require the full workflow unless it
changes an approved product, specification, test, or delivery input.

## Track Selection

Always run the Context Gate. Then state the selected track and why.

Use the **lightweight track** for local bug fixes, mechanical edits, narrow
configuration changes, and refactors with no new user-visible behavior or
cross-module contract.

Use the **full track** for:

- new or changed product behavior
- user-visible UI work
- API, schema, permission, state, or persistence changes
- changes spanning multiple ownership boundaries
- substantial refactors or new reusable abstractions
- work whose acceptance criteria are not already explicit

When uncertain, use the full track. A user may explicitly waive a review gate;
record the waiver and continue, but never waive fresh verification.

## Complexity and Regression Decision

Before selecting test scope, classify the change and state the rationale in
product-manager language. A change is **complex** when it affects a public
contract, data migration, permission or security boundary, critical business
path, or multiple module, role, or persistence boundaries. Otherwise it is
**non-complex** when its changed and affected behavior can be covered by
focused checks without those triggers.

- For a complex change, state the affected boundaries and ask the product owner
  whether to run full regression. Wait for the choice before committing to that
  scope; project policy can still require it.
- For a non-complex change, run focused tests for changed and affected behavior
  by default. Do not run full regression unless the user or project policy
  explicitly requires it.
- This decision does not waive TDD for behavioral code, targeted regression,
  or any verification required by a project policy.

## Context Gate

Complete these steps before editing code:

1. Locate the project root and read the nearest applicable `AGENTS.md`.
2. Read `ProjectGoal.md`. If absent, draft it from repository evidence and get
   product-owner approval before implementing. Update it only when the target
   users, outcome, milestone, success criteria, non-goals, or constraints
   changed.
3. Read `docs/ai/project-status.md` or the project-defined equivalent. Build
   missing status from code, tests, specifications, changelog, Git history, and
   current documentation. Mark unknown facts instead of guessing.
4. Run the code-map preflight described below.
5. Read the relevant mapped nodes, then inspect the referenced source, public
   interfaces, callers, tests, and documents with targeted searches.
6. Search for existing components, services, repositories, utilities,
   contracts, and test fixtures that own or nearly implement the requested
   behavior.
7. Compare the request with product goals, current progress, approved designs,
   OpenSpec changes, and implementation evidence.

Stop and ask the product owner when these sources conflict materially. Do not
silently choose one interpretation.

Before implementation, output a concise **Context Brief**:

- product goal and milestone served
- current product and implementation status
- code-map nodes and source evidence inspected
- existing capabilities to reuse, extend, or abstract
- selected track and planned modules
- user value, affected roles, scope, non-goals, and success measure
- blocking questions, decisions needed, and reversible assumptions
- complexity classification, affected boundaries, and regression choice
- specifications, designs, tests, and documents to create or update
- verification commands and delivery criteria
- unresolved assumptions or conflicts

## Code Map Preflight

Locate `scripts/code_map.py` relative to this `SKILL.md`; do not assume the
project contains a copy.

Default project files:

- `docs/ai/code-map.json`: machine-readable structural facts and semantic fields
- `docs/ai/code-map.md`: concise human/AI navigation view

Run:

```text
python <skill-directory>/scripts/code_map.py check --root <project-root> --json
```

- Status `missing`: run `bootstrap`.
- Status `stale`: run `update`, then inspect added, changed, and removed nodes.
- Status `fresh`: use mapped nodes to narrow source inspection.
- `pending_ai_review` does not make structure stale, but review relevant pending
  nodes before relying on their semantics.

After bootstrap or update:

1. Read product documents plus source and tests for relevant high-value nodes.
2. Enrich `product_capability`, `responsibility`, and `reuse_guidance` in
   `code-map.json`.
3. Set `needs_ai_review` to `false` only when those statements are evidence
   based.
4. Add AI semantic edges only when verified; use `"source": "ai"` and
   `"verified": true`.
5. Run `render`, then `check`.

The map is a navigation index. Always read files before modifying them. Do not
paste source bodies or map every private function into the map.

## Scope-First Global Logic

Complete the Global Logic Navigation defined in
`references/code-map-contract.md` before implementation. Include its verified
logic and impact slice in the Context Brief for cross-module or full-track
changes.

## Full-Track Design Gates

### Specification

For nontrivial behavior, invoke `$openspec-workflow` before implementation.
Create or update proposal, design, delta specifications, and tasks. Existing
OpenSpec artifacts must be reconciled rather than replaced with a parallel
plan.

Use relevant Superpowers process skills in this order:

1. `$brainstorming` for unclear behavior or design.
2. `$writing-plans` after the design is approved.
3. `$test-driven-development` during implementation.
4. `$systematic-debugging` for test or runtime failures.
5. `$verification-before-completion` before reporting success.

### Solution Review

For every material behavior or experience change, create a concise HTML
solution review artifact before implementation. Follow
`references/html-review-contract.md`. It must show the proposed user flow,
state or data flow as applicable, business rules, assumptions, unresolved
decisions, version, and approval status.

For UI changes, cover the complete affected experience: screens, navigation,
actions, states, validation, permissions, empty/loading/error behavior,
responsive behavior, and business logic. For material non-UI changes, use the
appropriate flow, state-machine, sequence, data-flow, or permission diagram.

Treat an artifact with unresolved material decisions or no explicit approval as
a proposal, not an approved development input. Do not silently drift from an
approved artifact; revise and re-review material changes.

### User-Scenario Test Review

Derive reviewable acceptance cases from `ProjectGoal.md`, OpenSpec, approved UI,
and current behavior. Cover the golden path, alternatives, boundary and extreme
values, errors and recovery, permissions, persistence, compatibility,
responsive behavior, and accessibility where applicable.

Present these cases in HTML before full-track implementation unless the product
owner explicitly waives pre-review.

## Implementation Gate

For behavioral changes, follow red-green-refactor:

1. Add or adjust a test that fails for the intended reason.
2. Implement the minimum behavior needed to pass.
3. Refactor only with passing tests.

Frontend:

- Inventory the canonical control before adding pagination, tables, selection,
  dialogs, forms, feedback, navigation, or layout primitives.
- Reuse the canonical component and states.
- If it is insufficient, improve its owning abstraction and migrate only the
  affected uses unless broader migration is approved.

Backend:

- Search existing services, repositories, domain methods, utilities, adapters,
  contracts, and fixtures first.
- Extend the current owner when it owns the behavior.
- When capabilities are nearly identical, extract the smallest coherent shared
  abstraction instead of creating parallel implementations.
- Preserve compatibility unless the approved specification changes it.

Update the code map during implementation only when module ownership, public
symbols, dependencies, routes, data boundaries, reusable components, or test
relationships change.

## Verification and Self-Repair

Run project-native unit, integration, contract, and acceptance checks. For
applicable web UI:

- use Playwright
- test user-visible behavior, not implementation details
- cover approved scenarios
- capture screenshots at meaningful checkpoints
- verify empty, loading, error, permission, and responsive states as applicable

When a required check fails:

1. Invoke `$systematic-debugging`.
2. identify the root cause
3. add or correct the reproducing test
4. fix the implementation
5. rerun the focused check
6. rerun the required broader suite

Continue until required checks pass. Report a genuine external blocker
explicitly; never represent skipped or failing evidence as passing.

## Latest-Build Gate

Before delivery:

1. Record current Git HEAD and dirty state.
2. stop or invalidate stale development servers and build output
3. build from the current source state
4. start or deploy that exact artifact
5. run acceptance tests against that artifact
6. record build command, timestamp, artifact/environment identity, source
   revision, dirty state, and test commands

Do not combine test results from one revision with an artifact from another.

Generate a conclusion-first HTML report when the full track or user-facing
testing applies. Include user-readable outcomes, scenario results, and
screenshots; link raw logs instead of making them the primary content.

## Documentation Impact Analysis

Complete the Documentation Impact Analysis defined in
`references/artifact-contract.md` after every code change.

## Documentation and Map Gate

Before completion:

1. run `code_map.py update`
2. review and enrich relevant new or changed nodes
3. run `render` and `check`
4. update `project-status.md`
5. complete the Documentation Impact Analysis
6. remove only documents confirmed as superseded or obsolete

Update `ProjectGoal.md` only when the actual product goal changed.

## Independent Delivery Audit

For every full-track change, complete the Independent Agent Audit defined in
`references/artifact-contract.md` before human handoff.

## Completion Gate

Invoke `$verification-before-completion` and run fresh final commands. Report:

- product outcome delivered
- reused or abstracted existing capabilities
- source modules and approved inputs changed
- user-scenario and automated test conclusions
- latest-build provenance
- code-map and documentation updates
- documentation-impact and independent-audit conclusions
- remaining risks or external blockers

Do not claim completion without fresh evidence.

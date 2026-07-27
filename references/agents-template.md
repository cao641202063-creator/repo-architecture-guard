# Project AGENTS.md Template

Place the following policy in the project-root `AGENTS.md`. Merge it with
project-specific architecture, commands, and conventions; project-specific
facts should be more concrete than this global default.

```md
## Mandatory Product and Repository Guard

Any task that may modify production code, tests, APIs, events, database
schemas, application configuration, feature flags, build behavior, deployment
behavior, shared UI components, or module boundaries MUST invoke
`$repo-architecture-guard` before analyzing implementation or editing files.

This requirement applies to every code change. The Skill may select a
lightweight or full track based on risk, but it may not skip the Context Gate
or fresh verification.

### Sources of Truth

Use these sources in order, resolving conflicts explicitly:

1. Explicit product-owner decisions in the current task
2. `ProjectGoal.md`
3. Approved OpenSpec changes and retained UI/test review artifacts
4. Current source code, public contracts, database definitions, and tests
5. `docs/ai/project-status.md`
6. `docs/ai/code-map.json` and `docs/ai/code-map.md`
7. Other current project documentation

Source code is authoritative for current implementation. The code map is a
navigation index and must never substitute for reading files that will change.

If product goals, approved design, documentation, tests, and implementation
conflict materially, stop before coding and present the conflict to the product
owner. Do not invent the intended behavior.

### Required Project Assets

Maintain these assets unless this project documents an explicit equivalent:

- `ProjectGoal.md`
- `docs/ai/project-status.md`
- `docs/ai/code-map.json`
- `docs/ai/code-map.md`
- `docs/ai/modules/` for complex-module notes only
- `docs/reviews/<change>-ui-review.html` for applicable UI review
- `docs/reviews/<change>-test-cases.html` for full-track acceptance review
- `artifacts/test-reports/<change>-report.html` for applicable delivery reports
- `openspec/changes/<change>/` for nontrivial behavior changes

`ProjectGoal.md` must define target users, product outcomes, current milestone,
success criteria, non-goals, constraints, and material product decisions. Read
it before every code task. Update it only when those facts change.

`docs/ai/project-status.md` must distinguish:

- product capabilities complete, partial, planned, or blocked
- implementation progress supported by code evidence
- automated and user-scenario test status
- documentation status and known obsolete items
- known gaps, risks, and next decisions

Unknown status must be labeled unknown; do not fill gaps by inference alone.

### Mandatory Context Brief

Before editing, output a concise Context Brief containing:

- product goal and current milestone served
- current product and implementation status
- code-map nodes, source, tests, and documents inspected
- existing components, methods, services, contracts, or fixtures to reuse
- selected lightweight or full track and why
- planned files, modules, specifications, designs, tests, and documents
- verification commands and delivery criteria
- unresolved assumptions or conflicts

Do not begin implementation until material conflicts have been resolved.

### Code Map Workflow

Before implementation:

1. Locate the installed `repo-architecture-guard/scripts/code_map.py`.
2. Run `check --root <project-root> --json`.
3. If missing, run `bootstrap`.
4. If stale, run `update` and inspect added, changed, and removed nodes.
5. Read only the relevant map nodes first, then inspect their linked source,
   callers, tests, and documentation with targeted searches.
6. Review relevant nodes whose `needs_ai_review` value is true.

After implementation:

1. Run `update`.
2. Review new and structurally changed high-value nodes.
3. Add evidence-based `product_capability`, `responsibility`, and
   `reuse_guidance`.
4. Set `needs_ai_review` to false only after checking source and tests.
5. Run `render`, then `check`.

Do not map every private function or copy source bodies into the map.

### Execution Tracks

Use the lightweight track only for narrow fixes, mechanical edits, local
refactors, and configuration changes with no new user-visible behavior or
cross-module contract.

Use the full track for new or changed product behavior, UI changes, APIs,
schemas, permissions, persistence, cross-module work, substantial refactors,
new shared abstractions, or unclear acceptance criteria.

Every track requires product alignment, current-state inspection, reuse
analysis, risk-proportionate tests, latest-source verification, and map/document
updates when affected.

### OpenSpec and Superpowers

Full-track work must invoke `$openspec-workflow` and reconcile the change with
existing OpenSpec artifacts before implementation.

Use relevant Superpowers process Skills:

- `$brainstorming` before creative or unclear design
- `$writing-plans` after design approval
- `$test-driven-development` for behavioral code
- `$systematic-debugging` for failures
- `$verification-before-completion` before success claims

Do not create a parallel specification or plan when an active OpenSpec change
already owns the work.

### Product and UI Review

For UI changes, create a concise HTML review artifact before coding. It must
show the complete affected experience, including:

- screens and navigation
- information hierarchy and actions
- normal, empty, loading, error, disabled, and permission states
- input rules, validation, feedback, and recovery
- data and business logic visible to the user
- responsive behavior and accessibility expectations

Retain the approved HTML as a development input. Material deviations require an
updated review.

Before full-track coding, generate an HTML user-scenario test matrix from
`ProjectGoal.md`, OpenSpec, approved UI, and current behavior. Cover golden,
alternative, boundary, extreme, error, recovery, permission, persistence,
compatibility, responsive, and accessibility scenarios where relevant.

The product owner may explicitly waive pre-implementation HTML review, but the
waiver must be recorded. Verification may not be waived.

### Implementation Rules

Use TDD for behavior changes: failing test, minimum passing implementation,
then refactor with passing tests.

Before adding frontend controls, identify the canonical project component for
pagination, tables, selection, dialogs, forms, feedback, navigation, and layout.
Reuse it. If it is insufficient, improve the owning component deliberately
instead of creating a competing variant.

Before adding backend behavior, search current services, repositories, domain
methods, utilities, adapters, contracts, and fixtures. Extend the current owner
when appropriate. When two capabilities are nearly identical, extract the
smallest coherent shared abstraction instead of building parallel methods.

Every changed line must trace to the approved requirement. Do not perform
unrelated cleanup or speculative architecture work.

### User-Scenario Verification

Run project-native unit, integration, contract, and acceptance tests. UI
acceptance tests must use Playwright when applicable and must verify user-visible
behavior rather than implementation details.

Capture screenshots at meaningful user-flow checkpoints. Reports should present
conclusions, scenario outcomes, and images first; raw logs are supporting
attachments.

Required test failures must form a closed loop:

1. reproduce
2. diagnose the root cause
3. add or correct the test
4. repair
5. rerun the focused check
6. rerun the required broader suite

Do not hand off a version with known required failures. Report genuine external
blockers explicitly instead of claiming success.

### Latest-Build Verification

Before delivery, record Git HEAD and dirty state, invalidate stale build output
and development servers, rebuild from the current source, and test that exact
artifact or environment.

The delivery report must record:

- source revision and dirty state
- build command and build time
- artifact hash, build ID, deployment ID, or equivalent environment identity
- test commands and result time
- acceptance scenario conclusions
- meaningful UI screenshots when applicable

Never combine test results from one revision with a build from another.

### Documentation Delivery Gate

Before delivery:

- update `docs/ai/project-status.md`
- update the code map and affected module notes
- update affected user and technical documentation
- inventory documentation and navigation
- remove documents confirmed as superseded or obsolete
- list ambiguous documents for product-owner review
- verify links, paths, commands, and examples

Update `ProjectGoal.md` only when the product goal, milestone, success criteria,
non-goals, constraints, or product decisions changed.

### Completion Standard

Do not claim completion until `$verification-before-completion` has been
invoked and fresh final commands have succeeded.

The final handoff must state:

- product outcome delivered
- existing capabilities reused or abstracted
- modules and approved inputs changed
- automated and user-scenario test conclusions
- exact latest-build provenance
- code-map and documentation updates
- residual risks or external blockers
```

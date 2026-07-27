# Human-Review HTML Contract

Create self-contained or project-runnable HTML that a product manager can
review without reading source code or raw test logs. Prefer concise text,
realistic data, diagrams, UI captures, and clear conclusions.

## UI Review Artifact

Store at `docs/reviews/<change>-ui-review.html`.

Include:

- product goal and affected users
- affected navigation and complete screen inventory
- realistic desktop and mobile states
- primary and alternative user flows
- data shown, actions available, and business rules
- field rules and validation feedback
- normal, empty, loading, disabled, error, recovery, and permission states
- component reuse decisions and any proposed canonical component change
- unresolved product decisions
- revision and approval status

The page is a development input, not a marketing page. Show the actual
experience. Keep technical implementation details out unless they change user
behavior.

## User-Scenario Test Artifact

Store at `docs/reviews/<change>-test-cases.html`.

Show a conclusion-first coverage summary and a filterable scenario table with:

- scenario ID
- requirement or product outcome
- persona or permission role
- preconditions and test data
- user steps
- expected user-visible result
- category: golden, alternative, boundary, extreme, error, recovery,
  permission, persistence, compatibility, responsive, or accessibility
- priority and risk
- automation target: unit, integration, contract, Playwright, or manual
- review status

Use enough cases to cover meaningful risk, not permutations with no additional
behavior. Explicitly show uncovered or intentionally excluded areas.

## Final Test Report

Store at `artifacts/test-reports/<change>-report.html`.

Order content for product review:

1. overall conclusion
2. delivered product outcome
3. scenario coverage and pass/fail/blocked counts
4. failed or blocked items and user impact
5. golden-flow narrative with screenshots
6. boundary, error, permission, and responsive conclusions
7. exact build provenance
8. supporting test commands and linked raw logs

Do not expose stack traces as the primary content. Translate failures into
user-visible impact. Include screenshots only when they demonstrate a state or
flow, and caption what the reviewer should notice.

## Latest-Build Evidence

The report must identify the exact tested artifact:

- source revision and dirty state
- build time and command
- artifact hash, build ID, deployment ID, or local server process
- environment or URL
- test completion time

If the build identity cannot be tied to the test run, the report is not valid.

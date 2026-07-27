# Product and Delivery Artifact Contract

Use project-defined equivalent paths when `AGENTS.md` maps them explicitly.

For a new project, generate the default assets with:

```text
python <skill-directory>/scripts/init_project.py --root <project-root>
```

The initializer preserves existing goal and status files by default and owns
only its marked block in `AGENTS.md`.

## ProjectGoal.md

Keep this document stable and product-facing:

```md
# Project Goal

## Target Users
## Product Outcome
## Current Milestone
## Success Criteria
## Non-Goals
## Constraints
## Product Decisions
```

Every statement must come from a product-owner decision or cited project
evidence. Record unknowns as decisions needed. Do not rewrite the file merely
to reflect implementation details.

## docs/ai/project-status.md

Use this as the current evidence-backed state:

```md
# Project Status

## Product Capability Status
## Implementation Status
## Test Status
## Documentation Status
## Known Gaps and Risks
## Next Product Decisions
## Evidence Snapshot
```

For each status item, include evidence paths, relevant tests or commands, and
the last verification date. Distinguish complete, partial, planned, blocked,
and unknown.

## Approved Development Inputs

Full-track changes may have:

- OpenSpec proposal, design, delta specs, and task list
- `<change>-ui-review.html`
- `<change>-test-cases.html`
- product-owner decisions recorded in project documentation

Treat approved inputs as versioned contracts. If implementation discovers a
material conflict, revise the owning input and return it for review before
continuing.

## Test Automation

Store executable tests using the project's established layout and framework.
The reviewable HTML scenario matrix is not a substitute for executable tests.
Each automated acceptance test should reference its scenario ID when the
framework supports names or tags.

## Latest-Build Provenance

Record these fields in the final report or an adjacent machine-readable result:

- source revision
- working-tree dirty state
- source fingerprint when no revision is available
- build command
- build start and completion time
- artifact path and hash, build ID, deployment ID, or environment URL
- server start command and process identity when testing locally
- test commands
- test completion time

Restart stale local servers and remove or invalidate stale build output using
the project's safe, documented command. Never delete an ambiguous directory.

## Documentation Inventory

Before full-track delivery, classify relevant documents:

- current
- needs update
- superseded, with replacement
- obsolete, with reason
- ambiguous, requiring product-owner decision

Delete only confirmed superseded or obsolete documents. Update indexes and
links in the same change. Keep user-facing navigation task-oriented rather than
organized solely by implementation modules.

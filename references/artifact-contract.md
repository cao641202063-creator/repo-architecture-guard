# Product and Delivery Artifact Contract

Use project-defined equivalent paths when `AGENTS.md` maps them explicitly.

## 语言

除非产品负责人或项目规则另有要求，所有面向人类的评审产物、场景矩阵、测试报告、
文档影响表和审计记录均以简体中文为主。命令、路径、文件名、代码、API 标识符、
配置键、JSON 字段及机器可读协议保持原文。

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
- `<change>-solution-review.html`
- `<change>-test-cases.html`
- product-owner decisions recorded in project documentation

Treat approved inputs as versioned contracts. If implementation discovers a
material conflict, revise the owning input and return it for review before
continuing.

## Solution Review Artifact

Store at `docs/reviews/<change>-solution-review.html`. Create one before
implementing every material behavior or experience change.

The artifact must show the product goal, affected users and roles, scope and
non-goals, proposed user flow, applicable state or data flow, business rules,
assumptions, unresolved decisions, version, and explicit approval status. For
UI work, include screens, navigation, validation, normal and exceptional
states, permissions, responsive behavior, and accessibility expectations. For
material non-UI work, include an appropriate flow, state-machine, sequence,
data-flow, or permission diagram.

An artifact with a material unresolved decision or no explicit approval is a
proposal, not an approved development input. A material implementation change
requires the artifact to be revised and reviewed again.

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

## Documentation Impact Analysis

After every code change, assess product, user, API or contract, operational,
technical, test, and navigation documentation. Record each relevant document
as updated, unchanged with evidence, superseded, obsolete, or requiring a
product-owner decision. Update affected documents and verify their links,
commands, paths, and examples.

For full-track work, include this table in the final test report. For
lightweight work, include the compact table in the final handoff. Do not create
a separate document solely to duplicate unchanged content.

## Independent Agent Audit

For a full-track change, retain an audit record in the final report when an
independent agent facility is available. The record must state the audit scope,
evidence reviewed, findings classified as blocker/major/minor/none, each
disposition, revisions, remaining risks, and unresolved decisions.

Give the independent agent a fresh context containing the request, approved
inputs, Context Brief, final diff, documentation-impact analysis, and
verification evidence. Its first pass is read-only and uses a distinct
checklist: requirement and approval traceability, missed affected boundaries,
regression scope, document dispositions, security or compatibility risk, and
unsupported delivery claims.

The primary agent makes at most one revision pass for blocker and major
findings, updates affected documents, and reruns applicable verification. Minor
findings may be accepted only with a stated reason. Do not start a second audit
loop unless the human requests it or verification fails. If no independent
agent facility is available, state that an explicit self-review was used
instead; do not describe it as an independent audit. The audit never replaces
product-owner or human approval.

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

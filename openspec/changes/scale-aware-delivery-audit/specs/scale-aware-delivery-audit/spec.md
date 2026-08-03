## Purpose

Enable efficient evidence-based understanding and independently audited,
documentation-complete delivery in large repositories.

## ADDED Requirements

### Requirement: Scope-first global logic navigation
Before reading implementation for a change, the Skill SHALL use the code map
and targeted repository evidence to identify the affected entry points, public
contracts, owners, dependencies, callers, persistence or event boundaries,
tests, and related documents. It SHALL produce a compact logic and impact
brief before reading additional files.

#### Scenario: Large repository change
- **WHEN** a change is requested in a repository with a current code map
- **THEN** the Skill SHALL begin with the relevant mapped nodes and traverse
  only evidence-backed adjacent boundaries instead of reading the repository
  indiscriminately

#### Scenario: Map cannot answer an impact question
- **WHEN** the code map lacks a required dependency, caller, or ownership fact
- **THEN** the Skill SHALL inspect targeted source and tests, update the map if
  its structural or semantic facts changed, and mark unknown facts explicitly

### Requirement: Documentation impact analysis
After every code change, the Skill SHALL assess the impact on product, user,
API or contract, operational, technical, test, and navigation documentation.
It SHALL update every affected document and record each assessed document as
updated, unchanged with evidence, superseded, obsolete, or requiring a product
owner decision.

#### Scenario: A document is affected
- **WHEN** a changed behavior, contract, workflow, configuration, or support
  procedure changes what a document says or how a user navigates it
- **THEN** the Skill SHALL update the document and verify its links, commands,
  paths, and examples

#### Scenario: No document content changes
- **WHEN** the documentation impact analysis finds no affected document
- **THEN** the final handoff SHALL record the assessed categories and the
  evidence for no update

### Requirement: Independent delivery audit
For every full-track change, when an independent-agent facility is available,
the Skill SHALL use a separate agent context to audit the completed change
before human review. The auditor SHALL not edit during its first pass and SHALL
return evidence-backed findings classified as blocker, major, minor, or none.

#### Scenario: Audit finds blocker or major issue
- **WHEN** the independent audit identifies a blocker or major issue
- **THEN** the primary agent SHALL make one revision pass, rerun applicable
  verification, and report the disposition of every finding to the human
  reviewer

#### Scenario: Independent agent is unavailable
- **WHEN** the execution environment cannot create an independent agent
  context
- **THEN** the Skill SHALL perform an explicit self-review, disclose that no
  independent audit occurred, and preserve the human review gate

#### Scenario: Audit completes
- **WHEN** the audit and any revision pass are complete
- **THEN** the human handoff SHALL include the audit scope, evidence reviewed,
  findings, revisions, remaining risks, and any unresolved decisions

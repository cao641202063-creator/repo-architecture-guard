## Purpose

Ensure product managers can turn incomplete change requests into explicit,
reviewable delivery decisions before engineering work starts.

## ADDED Requirements

### Requirement: Requirement readiness and product challenge
Before implementation planning, the Skill SHALL assess whether the request
states the user value, affected users, scope and exclusions, acceptance
criteria, business or data rules, permissions or failure behavior, constraints,
and priority where relevant. It SHALL surface contradictions with explicit
product decisions, goals, approved designs, and repository evidence.

#### Scenario: Blocking product information is missing
- **WHEN** a request lacks information that would materially change scope,
  behavior, acceptance, risk, or implementation approach
- **THEN** the Skill SHALL ask focused blocking questions and SHALL not begin
  implementation until the answers are available

#### Scenario: A request has a material conflict
- **WHEN** the requested change conflicts with a documented product decision,
  non-goal, approved design, or verified implementation evidence
- **THEN** the Skill SHALL explain the conflict, present the decision required,
  and SHALL not silently choose an interpretation

#### Scenario: A reversible detail is unknown
- **WHEN** a detail is unknown but does not materially change behavior or risk
- **THEN** the Skill SHALL record it as a reversible assumption for review

### Requirement: Proportional regression decision
The Skill SHALL classify a change as complex or non-complex before selecting
the regression scope. A complex change includes a public contract, data
migration, permission or security impact, critical business path, or multiple
affected module, role, or persistence boundaries.

#### Scenario: Complex change
- **WHEN** the assessment classifies a change as complex
- **THEN** the Skill SHALL explain the classification and ask the product owner
  whether to run full regression before implementation or delivery

#### Scenario: Non-complex change
- **WHEN** the assessment classifies a change as non-complex
- **THEN** the Skill SHALL run focused tests for the changed and affected
  behavior and SHALL not run full regression unless explicitly required by the
  user or project policy

### Requirement: Visual solution confirmation
For every material behavior or experience change, the Skill SHALL create a
reviewable visual solution artifact before implementation. The artifact SHALL
show the proposed user flow, state or data flow as applicable, business rules,
assumptions, unresolved decisions, version, and approval status.

#### Scenario: UI change
- **WHEN** a change affects a user interface
- **THEN** the visual solution artifact SHALL show the affected screens,
  navigation, states, validation, permissions, and responsive behavior

#### Scenario: Non-UI behavior change
- **WHEN** a material change does not affect a user interface
- **THEN** the visual solution artifact SHALL use an appropriate flow,
  state-machine, sequence, data-flow, or permission diagram

#### Scenario: Approval is absent
- **WHEN** the artifact contains material unresolved decisions or has not been
  explicitly approved
- **THEN** the Skill SHALL treat it as a proposal and SHALL not represent it as
  an approved development input

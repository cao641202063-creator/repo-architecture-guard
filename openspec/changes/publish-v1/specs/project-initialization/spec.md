# Project Initialization Specification

## ADDED Requirements

### Requirement: Capture Product Input

The initializer SHALL collect product name, target users, product outcome,
current milestone, success criteria, non-goals, and constraints from flags,
interactive prompts, or a business brief.

#### Scenario: Non-interactive initialization

- **WHEN** all required product fields are supplied as command arguments
- **THEN** initialization SHALL complete without reading interactive input
- **AND** `ProjectGoal.md` SHALL contain the supplied values

#### Scenario: Business brief initialization

- **WHEN** `--brief` references a readable UTF-8 file
- **THEN** the brief path and content SHALL be retained as product input
- **AND** missing structured fields SHALL be marked for product-owner review

### Requirement: Preserve Existing Project Policy

The initializer SHALL modify only its managed block in `AGENTS.md`.

#### Scenario: Existing unrelated policy

- **WHEN** `AGENTS.md` contains content outside the managed markers
- **THEN** initialization SHALL preserve that content
- **AND** append or replace exactly one managed block

#### Scenario: Repeated initialization

- **WHEN** initialization runs more than once
- **THEN** `AGENTS.md` SHALL contain exactly one managed block
- **AND** updated managed policy SHALL replace the previous managed policy

### Requirement: Preserve Existing Product Documents

The initializer SHALL preserve existing product goal and status documents by
default.

#### Scenario: Existing ProjectGoal

- **WHEN** `ProjectGoal.md` exists and `--force-goal` is absent
- **THEN** the file SHALL remain unchanged
- **AND** the result SHALL report it as preserved

### Requirement: Initialize Code Map

The initializer SHALL bootstrap a missing code map and update an existing map
unless `--no-code-map` is supplied.

#### Scenario: New project

- **WHEN** initialization runs without an existing map
- **THEN** `code_map.py bootstrap` SHALL run for the project root

#### Scenario: Documentation-only initialization

- **WHEN** `--no-code-map` is supplied
- **THEN** no code-map subprocess SHALL run

### Requirement: Report Results

The initializer SHALL report created, updated, preserved, and code-map actions.

#### Scenario: JSON automation

- **WHEN** `--json` is supplied
- **THEN** stdout SHALL contain valid JSON
- **AND** the process exit code SHALL indicate success or failure

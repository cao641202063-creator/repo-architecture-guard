# Project Goal

## Target Users

- Product managers who use AI coding agents but cannot efficiently audit large
  codebases.
- Developers and teams that want repeatable product, architecture, test, and
  documentation gates across multiple repositories.

## Product Outcome

Provide a reusable Codex Skill that makes every code change start from approved
product goals and verified repository context, favors existing architecture,
maintains a compact code map, challenges incomplete product requests, selects
proportionate regression scope, confirms material solutions visually, and
delivers evidence from the latest build.

## Current Milestone

Publish the Skill as the public GitHub repository
`cao641202063-creator/repo-architecture-guard` with an MIT license and a
`v1.1.0` release. Users must be able to install it with `npx skills` and
initialize a project through a guided command.

## Success Criteria

- `npx skills` can discover and install `repo-architecture-guard` from GitHub.
- A cross-platform Python command can create or safely merge `AGENTS.md`,
  `ProjectGoal.md`, and `docs/ai/project-status.md` from user business input.
- Initialization never overwrites unrelated existing `AGENTS.md` content.
- Initialization can bootstrap or refresh the repository code map.
- Code-map and initializer automated tests pass on Windows and GitHub Actions.
- Incomplete, contradictory, or materially ambiguous requests produce focused
  product questions or decision options before implementation.
- Complex changes request a product-owner choice about full regression;
  non-complex changes default to focused verification.
- Material UI and non-UI designs have a reviewable visual solution artifact
  with explicit approval status.
- Large repositories use code-map-guided, scope-first traversal to establish
  global logic and change impact without indiscriminate rereading.
- Every completed code change records documentation impact and updates affected
  documents; full-track delivery includes an independent-agent audit when the
  environment supports it.
- GitHub contains a public `v1.1.0` release with clear installation, update,
  initialization, and usage instructions.

## Non-Goals

- Replace OpenSpec, Superpowers, Playwright, or project-native test frameworks.
- Generate final product decisions without user input or evidence.
- Rewrite project-specific `AGENTS.md` policies outside the managed block.
- Require network access or third-party Python packages at Skill runtime.

## Constraints

- Runtime scripts must use only the Python standard library.
- Windows, macOS, and Linux must be supported.
- Source code remains authoritative; generated maps are navigation aids.
- Existing project files must be preserved unless the user explicitly approves
  replacement or deletion.
- Human-facing Skill outputs and review artifacts default to Simplified Chinese;
  commands, paths, code, and machine-readable fields remain unchanged.

## Product Decisions

- Repository visibility: public.
- License: MIT.
- Current release target: `v1.1.0`.
- Installation channel: `npx skills`.
- Initialization UX: interactive prompts plus non-interactive flags and a
  business-brief file option.
- `AGENTS.md` integration: replace only a clearly marked managed block.

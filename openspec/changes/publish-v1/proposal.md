# Publish Repository Architecture Guard v1.0.0

## Why

The Skill currently works only as a local installation. Product managers need
to reuse it across repositories and initialize project governance without
manually assembling `AGENTS.md`, `ProjectGoal.md`, status, and code-map files.

## What Changes

- Publish the Skill from a public GitHub repository under the MIT license.
- Add a cross-platform, standard-library project initialization command.
- Support interactive input, non-interactive flags, and business-brief files.
- Merge a managed policy block into existing `AGENTS.md` content safely.
- Create missing product goal and project status documents without overwriting
  existing user content.
- Optionally bootstrap or update the code map.
- Add installation, update, initialization, and usage documentation.
- Add CI and a tagged `v1.0.0` release.

## Impact

- New script: `scripts/init_project.py`
- New tests: `tests/test_init_project.py`
- Updated code-map scanner and tests
- New README, license, workflow, and release documentation
- New generated governance artifacts for this Skill repository

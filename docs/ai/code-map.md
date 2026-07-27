# Code Map

> Generated structural facts. Source code remains authoritative.

## Repository

- Project: `repo-architecture-guard`
- Generated: `2026-07-27T09:24:41Z`
- Source HEAD: `69f9de81176c6fbfb9df070ddf5ce1caa3cd1702`
- Working tree dirty: `yes`
- Stacks: `python`
- Nodes: `17`

Run `code_map.py check --root .` before coding and `update` after structural changes.

## Module

### `module.scripts` - scripts

- Paths: `scripts/code_map.py`, `scripts/init_project.py`
- Product capability: Cross-project governance initialization and repository code-map maintenance.
- Responsibility: Owns deterministic project scaffolding, safe AGENTS managed-block merging, code-map discovery, freshness checks, updates, and rendering.
- Reuse guidance: Invoke init_project.py for new projects and code_map.py before and after code changes; do not duplicate their file-protection or fingerprint logic in project-specific scripts.
- Notes: Covered by tests/test_init_project.py, tests/test_code_map.py, and tests/test_package.py.

## Test

### `tests.test.code.map` - CodeMapWorkflowTests

- Paths: `tests/test_code_map.py`
- Public symbols: `CodeMapWorkflowTests`, `setUp`, `tearDown`, `test_bootstrap_builds_typed_nodes_and_markdown`, `test_check_and_update_detect_added_and_removed_nodes`, `test_check_detects_source_change_and_update_preserves_semantics`, `test_render_uses_enriched_json`

### `tests.test.init.project` - ProjectInitializerTests

- Paths: `tests/test_init_project.py`
- Public symbols: `ProjectInitializerTests`, `setUp`, `tearDown`, `test_business_brief_is_retained_and_missing_fields_are_explicit`, `test_code_map_is_bootstrapped_for_new_project`, `test_existing_agents_content_is_preserved_and_block_is_idempotent`, `test_existing_goal_and_status_are_preserved_without_force`, `test_force_flags_replace_existing_goal_and_status`, `test_missing_business_brief_fails_before_writing_files`, `test_non_interactive_initialization_creates_business_documents`

### `tests.test.package` - SkillPackageTests

- Paths: `tests/test_package.py`
- Public symbols: `SkillPackageTests`, `test_readme_documents_install_update_and_initialization`, `test_required_distribution_files_exist`, `test_skill_frontmatter_has_expected_name_and_description`

## Documentation

### `agents` - AGENTS

- Paths: `AGENTS.md`

### `docs.ai.project.status` - project-status

- Paths: `docs/ai/project-status.md`

### `openspec.changes.publish.v1.design` - design

- Paths: `openspec/changes/publish-v1/design.md`

### `openspec.changes.publish.v1.proposal` - proposal

- Paths: `openspec/changes/publish-v1/proposal.md`

### `openspec.changes.publish.v1.specs.project.initialization.spec` - spec

- Paths: `openspec/changes/publish-v1/specs/project-initialization/spec.md`

### `openspec.changes.publish.v1.tasks` - tasks

- Paths: `openspec/changes/publish-v1/tasks.md`

### `projectgoal` - ProjectGoal

- Paths: `ProjectGoal.md`

### `readme` - README

- Paths: `README.md`

### `references.agents.template` - agents-template

- Paths: `references/agents-template.md`

### `references.artifact.contract` - artifact-contract

- Paths: `references/artifact-contract.md`

### `references.code.map.contract` - code-map-contract

- Paths: `references/code-map-contract.md`

### `references.html.review.contract` - html-review-contract

- Paths: `references/html-review-contract.md`

### `skill` - SKILL

- Paths: `SKILL.md`

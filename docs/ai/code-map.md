# Code Map

> Generated structural facts. Source code remains authoritative.

## Repository

- Project: `repo-architecture-guard`
- Generated: `2026-08-03T02:09:41Z`
- Source HEAD: `341ea8eaeed2cf1156e5f481861f8f482042e32d`
- Working tree dirty: `yes`
- Stacks: `python`
- Nodes: `29`

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
- Product capability: Prevents distribution and governance-policy regressions in the published Skill.
- Responsibility: Verifies package files, installation documentation, and essential policy wording across governed documents.
- Public symbols: `SkillPackageTests`, `test_governance_policy_requires_product_readiness_and_proportional_testing`, `test_governance_policy_requires_scale_aware_impact_and_independent_audit`, `test_human_facing_artifacts_default_to_simplified_chinese`, `test_readme_documents_install_update_and_initialization`, `test_required_distribution_files_exist`, `test_skill_frontmatter_has_expected_name_and_description`
- Reuse guidance: Extend when a cross-document mandatory rule is added or renamed.
- Notes: Includes the strengthen-pm-governance policy contract test.

## Documentation

### `agents` - AGENTS

- Paths: `AGENTS.md`
- Product capability: Applies the repository's own governance rules when the Skill is changed.
- Responsibility: Requires context inspection, TDD for runtime code, and full repository verification before publishing.
- Reuse guidance: Read before changing this repository; its rules override generic Skill defaults.
- Notes: Repository-local policy.

### `docs.ai.project.status` - project-status

- Paths: `docs/ai/project-status.md`

### `openspec.changes.chinese.first.language.design` - design

- Paths: `openspec/changes/chinese-first-language/design.md`

### `openspec.changes.chinese.first.language.proposal` - proposal

- Paths: `openspec/changes/chinese-first-language/proposal.md`

### `openspec.changes.chinese.first.language.specs.chinese.first.language.spec` - spec

- Paths: `openspec/changes/chinese-first-language/specs/chinese-first-language/spec.md`

### `openspec.changes.chinese.first.language.tasks` - tasks

- Paths: `openspec/changes/chinese-first-language/tasks.md`

### `openspec.changes.publish.v1.design` - design

- Paths: `openspec/changes/publish-v1/design.md`

### `openspec.changes.publish.v1.proposal` - proposal

- Paths: `openspec/changes/publish-v1/proposal.md`

### `openspec.changes.publish.v1.specs.project.initialization.spec` - spec

- Paths: `openspec/changes/publish-v1/specs/project-initialization/spec.md`

### `openspec.changes.publish.v1.tasks` - tasks

- Paths: `openspec/changes/publish-v1/tasks.md`

### `openspec.changes.scale.aware.delivery.audit.design` - design

- Paths: `openspec/changes/scale-aware-delivery-audit/design.md`

### `openspec.changes.scale.aware.delivery.audit.proposal` - proposal

- Paths: `openspec/changes/scale-aware-delivery-audit/proposal.md`

### `openspec.changes.scale.aware.delivery.audit.specs.scale.aware.delivery.audit.spec` - spec

- Paths: `openspec/changes/scale-aware-delivery-audit/specs/scale-aware-delivery-audit/spec.md`

### `openspec.changes.scale.aware.delivery.audit.tasks` - tasks

- Paths: `openspec/changes/scale-aware-delivery-audit/tasks.md`

### `openspec.changes.strengthen.pm.governance.design` - design

- Paths: `openspec/changes/strengthen-pm-governance/design.md`

### `openspec.changes.strengthen.pm.governance.proposal` - proposal

- Paths: `openspec/changes/strengthen-pm-governance/proposal.md`

### `openspec.changes.strengthen.pm.governance.specs.pm.governance.spec` - spec

- Paths: `openspec/changes/strengthen-pm-governance/specs/pm-governance/spec.md`

### `openspec.changes.strengthen.pm.governance.tasks` - tasks

- Paths: `openspec/changes/strengthen-pm-governance/tasks.md`

### `projectgoal` - ProjectGoal

- Paths: `ProjectGoal.md`
- Product capability: Defines the product-manager governance outcome and success criteria for the Skill.
- Responsibility: Records product decisions for request readiness, proportional regression, and visual solution review.
- Reuse guidance: Use it to judge whether a request serves the product outcome before changing delivery rules.
- Notes: Updated for the strengthen-pm-governance change.

### `readme` - README

- Paths: `README.md`

### `references.agents.template` - agents-template

- Paths: `references/agents-template.md`
- Product capability: Propagates product-manager governance into initialized repositories.
- Responsibility: Defines the generated AGENTS policy for readiness, complexity, visual review, and verification.
- Reuse guidance: Modify in lockstep with SKILL.md and validate policy contract tests.
- Notes: Loaded by init_project.py into the managed AGENTS block.

### `references.artifact.contract` - artifact-contract

- Paths: `references/artifact-contract.md`
- Product capability: Makes solution review and delivery evidence usable by product managers.
- Responsibility: Defines approved inputs, HTML solution review, tests, provenance, and document inventory.
- Reuse guidance: Use alongside the HTML contract when creating a material-change review artifact.
- Notes: Supports UI and non-UI solution confirmation.

### `references.code.map.contract` - code-map-contract

- Paths: `references/code-map-contract.md`

### `references.html.review.contract` - html-review-contract

- Paths: `references/html-review-contract.md`
- Product capability: Provides a visual confirmation surface for material product changes.
- Responsibility: Specifies the self-contained HTML solution review and test-report content.
- Reuse guidance: Choose UI screens or a non-UI flow, state, sequence, data, or permission diagram as applicable.
- Notes: Approval status and material unresolved decisions determine whether it is an approved input.

### `skill` - SKILL

- Paths: `SKILL.md`
- Product capability: Guides product-goal-driven, repository-aware software delivery.
- Responsibility: Orchestrates readiness, architecture context, complexity, visual review, implementation, and verification gates.
- Reuse guidance: Invoke before code changes; use the referenced policy and artifact contracts instead of duplicating the workflow.
- Notes: Strengthened with product challenge and proportional regression rules.

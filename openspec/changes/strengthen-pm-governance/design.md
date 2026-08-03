## Context

See `proposal.md` for motivation. The current workflow has a Context Brief and
UI-specific HTML review, but it does not define a request-completeness check,
complexity decision, or non-UI visual review contract. Equivalent delivery
rules are duplicated in `SKILL.md` and the generated `AGENTS.md` template.

## Goals / Non-Goals

**Goals:**

- Make ambiguity and conflicts visible to the product owner before coding.
- Select regression scope proportionally without weakening focused validation.
- Preserve a human-readable approval point for UI and non-UI product changes.
- Keep the canonical Skill, generated policy, and artifact contracts aligned.

**Non-Goals:**

- Automate product decisions or infer missing business rules.
- Replace project-native test commands, OpenSpec, or TDD for behavioral code.
- Require full regression for every change.

## Decisions

### One explicit readiness gate with three outcomes

The workflow will classify gaps as blocking questions, decisions needing an
owner choice, or reversible assumptions. This makes the agent decisive without
inventing behavior. A numeric readiness score was rejected because a checklist
with materiality judgment is clearer and less gameable.

### Conservative complexity triggers and explicit regression consent

Any public contract, migration, permission/security impact, critical business
path, or multiple affected module/role/persistence boundaries makes a change
complex. Complex changes prompt for full regression; non-complex changes run
focused checks by default. Project policy and an explicit user request override
the default.

### One solution-review contract, with medium chosen by change type

The existing self-contained HTML review artifact remains the review surface.
UI changes use screen and flow representations; non-UI changes use a flow,
state, sequence, data, or permission representation. A separate artifact type
was rejected because it would duplicate approval and retention behavior.

## Risks / Trade-offs

- More up-front questions can slow small tasks → only material missing facts
  block; reversible assumptions remain lightweight.
- A complex classification may over-test or under-test → require the rationale
  and allow project policy or the product owner to override it.
- Duplicated policy can drift → add tests that assert the essential rules exist
  in each generated surface.

## Migration Plan

Update the canonical Skill, generated policy, contracts, README, and product
goal together. Existing initialized projects adopt the policy on their next
initializer run; no user-owned text outside the managed block changes.

## Why

Product managers need the Skill to identify an incomplete or contradictory
request before engineering work begins, not merely detect conflicts between
repository artifacts. They also need a proportionate testing decision and a
reviewable representation of every material solution, including non-UI work.

## What Changes

- Add a mandatory requirement-readiness and product-challenge gate before
  implementation planning.
- Add a deterministic complex-change assessment and a user decision gate for
  full-regression testing.
- Extend pre-implementation visual review from UI-only artifacts to a solution
  review artifact for material non-UI behavior.
- Make the Context Brief and generated project policy communicate product value,
  scope, decisions, risks, and test strategy in product-manager language.
- Add package-level policy contract tests and synchronize the code map.

## Capabilities

### New Capabilities
- `pm-governance`: Requirement readiness, product challenge, proportional test
  selection, visual solution-confirmation behavior, and generated project
  policy for the Skill.

### Modified Capabilities

- None.

## Impact

The change updates the Skill, reusable project policy, review artifact
contracts, product documentation, package tests, and the code-map metadata. It
adds no runtime dependency and preserves the standard-library-only initializer.

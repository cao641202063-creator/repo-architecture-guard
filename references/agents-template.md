# Project AGENTS.md Template

Merge this policy with project-specific architecture, commands, and conventions. Project facts and required checks override this default.

```md
## Mandatory Product and Repository Guard

Before modifying production code, tests, APIs, events, database schemas, configuration, build/deployment behavior, shared UI, or module boundaries, invoke `$repo-architecture-guard`.

It must complete a focused Context Gate: read applicable project rules, product goal, current status, relevant active specification, and code-map nodes; then inspect the actual owner, callers, contracts, tests, and documentation. Source remains authoritative.

### Sources of Truth

1. Explicit product-owner decision in the current task
2. `ProjectGoal.md`
3. Active Trellis task **or** approved OpenSpec change
4. Current source, contracts, schemas, and tests
5. Project status and code map
6. Other current documentation

Stop for material conflicts. Record reversible assumptions rather than inventing behavior.

### One System of Record

- Use Trellis for long personal/small-team work and cross-session handoffs.
- Use OpenSpec for formal, shared, or multi-repository requirements.
- Never create parallel PRDs or plans in both systems.
- Use Grill-me only to clarify material ambiguity before selecting the record.
- Use individual Superpowers skills only when their capability is needed.

### Risk-Based Verification

Classify the change before editing:

- **L0**: mechanical/documentation/style work — relevant lint, format, or build check.
- **L1**: isolated module change — `test:changed` plus applicable lint/type-check.
- **L2**: cross-module, UI flow, state/persistence, API/event contract, or shared abstraction — focused + integration/contract + one final smoke pass.
- **L3**: security/permission, payment, migration, shared infrastructure, critical path, or explicit policy trigger — L2 checks plus one final full regression and independent audit when available.

Use project-native commands. Do not run full regression after each edit. Rerun focused checks during implementation and the selected broader suite once on the final candidate.

### Review and Handoff

Require HTML solution or scenario review only for L2/L3 changes that materially alter product behavior, user flows, rules, permissions, or state/data flow. Build and test the final artifact once when L2/L3 or project policy requires it.

Report the impact evidence, selected workflow, risk level, commands actually run, skipped gates and reasons, document/code-map updates, and residual risks. Never describe skipped checks as passing.
`

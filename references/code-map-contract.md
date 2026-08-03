# Code Map Contract

## Files

- `docs/ai/code-map.json`: source for machines and AI enrichment
- `docs/ai/code-map.md`: generated concise navigation view
- `docs/ai/modules/*.md`: optional details for genuinely complex modules

Do not manually maintain structural facts in Markdown. Change semantic fields
in JSON and run `render`.

## Commands

Resolve the script from the installed Skill directory:

```text
python <skill-directory>/scripts/code_map.py bootstrap --root <project-root>
python <skill-directory>/scripts/code_map.py check --root <project-root> --json
python <skill-directory>/scripts/code_map.py update --root <project-root>
python <skill-directory>/scripts/code_map.py render --root <project-root>
```

`bootstrap` creates a missing map. `check` returns exit code `0` when fresh,
`1` when missing or stale, and `2` for invalid input or malformed map.
`update` rescans deterministic facts while preserving semantic fields for stable
node IDs. `render` regenerates Markdown from JSON.

## Node Selection

Create nodes only for stable navigation, ownership, reuse, data, and
verification boundaries:

- module
- application entry
- page or route
- component
- API or controller
- service or use case
- domain entity or aggregate
- repository or data model
- external integration
- worker, consumer, or scheduled job
- application state
- test
- documentation

Do not create one node per private function. Private details belong in source.

## Node Fields

Structural fields are script owned:

- `id`
- `type`
- `name`
- `paths`
- `symbols`
- `imports`
- `dependencies`
- `tests`
- `fingerprint`
- `last_verified`

Semantic fields are AI/human owned and preserved by `update`:

- `product_capability`
- `responsibility`
- `reuse_guidance`
- `notes`
- `needs_ai_review`

Write semantic fields only after reading product evidence, source, public
interfaces, callers, and tests. Use short factual sentences. Do not infer
aspirational behavior from names alone.

## Edges

The script creates verified `imports` edges where local resolution is
deterministic. AI may add verified semantic edges:

- `implements`
- `calls`
- `renders`
- `reads`
- `writes`
- `publishes`
- `consumes`
- `tests`
- `documents`
- `reuses`

AI edges must have:

```json
{
  "from": "source.node",
  "to": "target.node",
  "type": "calls",
  "source": "ai",
  "verified": true
}
```

Do not add speculative edges.

## Initial Enrichment

After `bootstrap`:

1. Start with nodes relevant to the current product task.
2. Read `ProjectGoal.md`, status, OpenSpec, and relevant user documentation.
3. Read each node's source, public symbols, callers, and tests.
4. Add product capability, responsibility, and reuse guidance.
5. Mark reviewed nodes `needs_ai_review: false`.
6. Run `render` and `check`.

It is acceptable for unrelated nodes to remain pending. Do not spend tokens
enriching the entire repository when the task does not need them.

## Global Logic Navigation

For a code change, start from the code-map nodes nearest to the requested
behavior. State a compact scope hypothesis: entry points, public contracts,
owners, direct dependencies, callers, data or event boundaries, tests, and
documents likely affected.

Then verify only the required adjacent boundaries through targeted source,
caller, test, and document inspection. Expand the scope when evidence requires
it; mark unknowns rather than inferring them. The map is navigation evidence,
not proof of behavior, and never replaces reading changed files. Include the
verified logic and impact slice in the Context Brief. Do not read the repository
indiscriminately or create a second global map.

Use `docs/ai/modules/` only for a genuinely complex module whose local map node
cannot explain its stable responsibilities and boundaries. Do not duplicate
code-map facts, source bodies, or per-change analysis in module notes.

## Update Rules

Run `check` before coding and `update` after structural changes.

Review a node again when:

- its public symbols change
- its ownership or responsibility changes
- its dependencies or test coverage change materially
- a route, API, schema, event, or persistence boundary changes
- it becomes or ceases to be the canonical reusable implementation

Internal behavior changes that preserve ownership and public contracts usually
need only a new fingerprint and test evidence.

Use a full semantic rebuild only after:

- large directory or package migration
- technology-stack replacement
- widespread invalid or orphan nodes
- map corruption
- explicit product-owner request

## Token Control

Use this reading order:

1. `ProjectGoal.md`
2. relevant section of `project-status.md`
3. code-map metadata and relevant node entries
4. source and tests linked by those nodes
5. targeted callers and dependencies

Do not read every module note or every mapped file by default. The map reduces
broad discovery; it does not reduce the need to read code being changed.

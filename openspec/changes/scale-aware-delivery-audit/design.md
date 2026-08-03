## Context

See `proposal.md` for motivation. The current code map already provides stable
nodes and semantic edges, while the documentation gate lists inventory actions.
Neither contract defines a compact system-slice brief, a per-change document
impact disposition, or an independent audit with bounded iteration.

## Goals / Non-Goals

**Goals:**

- Increase global understanding through progressive, evidence-backed traversal.
- Make documentation consequences visible and verifiable at delivery.
- Add a useful independent review without recursive multi-agent churn.

**Non-Goals:**

- Read every source file or duplicate the repository map in a new artifact.
- Treat an independent agent as a substitute for human approval.
- Run a multi-agent audit for lightweight changes by default.

## Decisions

### Reuse the code map; add a logic-and-impact brief

The map remains the navigation index. The primary agent starts from affected
nodes, follows only verified adjacent boundaries, and reports entry points,
contracts, ownership, dependencies, callers, data or event boundaries, tests,
and documents. A second global map would duplicate facts and become stale.

### Persist full-track documentation analysis with existing delivery evidence

The final test report gains a documentation-impact section. It records each
relevant document category and a disposition. Lightweight changes carry the
same compact section in the final handoff, avoiding a new file for every small
edit.

### Use one independent auditor and one bounded revision pass

The primary agent implements. A newly started independent agent receives the
request, approved inputs, diff, verification evidence, and a fixed checklist;
it inspects without editing. The primary agent resolves blocker and major
findings once, then reruns verification. Minor findings can be accepted with a
reason. A second auditor or loop occurs only on explicit human request or a
failed verification.

### Make delegation capability-aware

The policy says to use an independent context when the environment supports
one. If unavailable, it requires an explicit self-review and disclosure rather
than pretending a separate audit occurred.

## Risks / Trade-offs

- Map inaccuracies can narrow the wrong slice → inspect source before editing,
  preserve unknowns, and update affected map facts.
- Audit costs time and tokens → require it for full-track work only and limit
  it to one targeted pass.
- Auditors may repeat the primary agent's reasoning → give the audit a
  different checklist focused on requirement traceability, impact, tests,
  documents, and unproven claims.

## Migration Plan

Add the shared rules to the canonical Skill and generated policy, put
map-specific rules in the code-map contract, and put impact/audit evidence in
the artifact contract. Existing initialized projects receive the revised policy
when their managed block is next refreshed.

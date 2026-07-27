# Design

## Initializer Boundary

`scripts/init_project.py` owns deterministic project scaffolding. It does not
interpret business strategy. It records user input as product evidence and
creates a structured draft for subsequent product-owner and AI review.

## Input Modes

- Interactive prompts when required flags are absent and stdin is interactive.
- Non-interactive flags for automation.
- `--brief <path>` to retain an existing UTF-8 business document as evidence.
- `--no-code-map` to skip map execution when initialization must remain
  documentation-only.

## Safe Merge

The initializer owns only the content between:

```text
<!-- repo-architecture-guard:start -->
<!-- repo-architecture-guard:end -->
```

When the block exists, it is replaced in place. When absent, it is appended
after existing content. Content outside the markers is byte-for-byte preserved
apart from ensuring one separating newline.

Existing `ProjectGoal.md` and `project-status.md` are never overwritten by
default. `--force-goal` and `--force-status` are explicit replacement controls.

## Code Map Integration

The initializer resolves `code_map.py` beside itself. A missing map runs
`bootstrap`; an existing map runs `update`. Failures return a nonzero exit code
and leave already written product files intact with a clear message.

## Output

The command prints a concise summary of created, updated, preserved, and
code-map actions. `--json` emits the same information as structured JSON.

## Distribution

The GitHub repository root is the Skill root so `npx skills add` discovers it
without `--full-depth`. Runtime remains Python standard-library only.

#!/usr/bin/env python3
"""Initialize product and repository governance for a project."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


START_MARKER = "<!-- repo-architecture-guard:start -->"
END_MARKER = "<!-- repo-architecture-guard:end -->"
UNKNOWN = "Needs product-owner review."


def normalize_root(value: str) -> Path:
    root = Path(value).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Project root does not exist or is not a directory: {root}")
    return root


def read_preserving_newlines(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def atomic_write(path: Path, content: str, newline: str = "\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        handle.write(content.replace("\n", newline) if newline != "\n" else content)
    temporary.replace(path)


def split_items(value: str | None) -> list[str]:
    if not value:
        return []
    return [
        item.strip()
        for item in re.split(r"[\r\n;；]+", value)
        if item.strip()
    ]


def markdown_list(value: str | None) -> str:
    items = split_items(value)
    if not items:
        return f"- {UNKNOWN}"
    return "\n".join(f"- {item}" for item in items)


def inline_value(value: str | None) -> str:
    items = split_items(value)
    return "; ".join(items) if items else UNKNOWN


def resolve_brief(root: Path, value: str | None) -> tuple[Path | None, str]:
    if not value:
        return None, ""
    candidate = Path(value).expanduser()
    if not candidate.is_absolute():
        root_candidate = root / candidate
        candidate = root_candidate if root_candidate.exists() else Path.cwd() / candidate
    candidate = candidate.resolve()
    if not candidate.exists() or not candidate.is_file():
        raise ValueError(f"Business brief does not exist or is not a file: {candidate}")
    try:
        return candidate, candidate.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"Business brief must be UTF-8: {candidate}") from exc


def prompt_if_missing(label: str, current: str | None) -> str | None:
    if current:
        return current
    value = input(f"{label}: ").strip()
    return value or None


def collect_input(args: argparse.Namespace, root: Path, has_brief: bool) -> dict[str, str | None]:
    values = {
        "project_name": args.project_name or root.name,
        "target_users": args.target_users,
        "outcome": args.outcome,
        "milestone": args.milestone,
        "success_criteria": args.success_criteria,
        "non_goals": args.non_goals,
        "constraints": args.constraints,
    }
    missing = [
        key
        for key in ("target_users", "outcome", "milestone", "success_criteria")
        if not values[key]
    ]
    if missing and not has_brief:
        if not sys.stdin.isatty():
            flags = ", ".join("--" + key.replace("_", "-") for key in missing)
            raise ValueError(
                f"Missing required business input in non-interactive mode: {flags}. "
                "Provide the fields or use --brief."
            )
        labels = {
            "target_users": "Target users",
            "outcome": "Product outcome",
            "milestone": "Current milestone",
            "success_criteria": "Success criteria (separate items with semicolons)",
            "non_goals": "Non-goals (optional)",
            "constraints": "Constraints (optional)",
        }
        for key in (
            "target_users",
            "outcome",
            "milestone",
            "success_criteria",
            "non_goals",
            "constraints",
        ):
            values[key] = prompt_if_missing(labels[key], values[key])
    return values


def quote_brief(text: str) -> str:
    lines = text.rstrip().splitlines()
    return "\n".join("> " + line if line else ">" for line in lines)


def render_goal(
    values: dict[str, str | None],
    brief_path: Path | None,
    brief_text: str,
) -> str:
    evidence = ""
    if brief_path:
        evidence = (
            "\n## Business Brief Evidence\n\n"
            f"Source: `{brief_path}`\n\n"
            f"{quote_brief(brief_text)}\n"
        )
    return (
        f"# Project Goal: {values['project_name']}\n\n"
        "## Target Users\n\n"
        f"{markdown_list(values['target_users'])}\n\n"
        "## Product Outcome\n\n"
        f"{values['outcome'] or UNKNOWN}\n\n"
        "## Current Milestone\n\n"
        f"{values['milestone'] or UNKNOWN}\n\n"
        "## Success Criteria\n\n"
        f"{markdown_list(values['success_criteria'])}\n\n"
        "## Non-Goals\n\n"
        f"{markdown_list(values['non_goals'])}\n\n"
        "## Constraints\n\n"
        f"{markdown_list(values['constraints'])}\n\n"
        "## Product Decisions\n\n"
        "- Product-owner decisions must be recorded here before implementation "
        "depends on them.\n"
        f"{evidence}"
    )


def render_status(values: dict[str, str | None], brief_path: Path | None) -> str:
    evidence = (
        f"- Business brief: `{brief_path}`\n" if brief_path else "- Interactive or command-line product input.\n"
    )
    return (
        "# Project Status\n\n"
        "## Product Capability Status\n\n"
        "- Initialization completed; capability status requires repository review.\n\n"
        "## Implementation Status\n\n"
        "- Current implementation status is unknown until code-map and source review.\n\n"
        "## Test Status\n\n"
        "- Current automated and user-scenario test status is unknown.\n\n"
        "## Documentation Status\n\n"
        "- Product goal and repository guard initialized.\n"
        "- Remaining documentation requires inventory and evidence review.\n\n"
        "## Known Gaps and Risks\n\n"
        "- AI must inspect current source, tests, specifications, and documents "
        "before changing code.\n\n"
        "## Next Product Decisions\n\n"
        f"- Confirm the current milestone: {values['milestone'] or UNKNOWN}\n\n"
        "## Evidence Snapshot\n\n"
        f"{evidence}"
    )


def load_agents_policy(skill_root: Path) -> str:
    template_path = skill_root / "references" / "agents-template.md"
    text = template_path.read_text(encoding="utf-8")
    match = re.search(r"```md\r?\n(.*?)\r?\n```", text, re.DOTALL)
    if not match:
        raise ValueError(f"Cannot extract AGENTS policy from: {template_path}")
    return match.group(1).strip()


def render_managed_block(
    values: dict[str, str | None],
    brief_path: Path | None,
    policy: str,
) -> str:
    context = [
        START_MARKER,
        "## Project-Specific Product Context",
        "",
        f"- Project: {values['project_name']}",
        f"- Target users: {inline_value(values['target_users'])}",
        f"- Product outcome: {values['outcome'] or UNKNOWN}",
        f"- Current milestone: {values['milestone'] or UNKNOWN}",
    ]
    if brief_path:
        context.append(f"- Business brief: `{brief_path}`")
    context.extend(["", policy, END_MARKER])
    return "\n".join(context)


def merge_agents(path: Path, block: str) -> tuple[str, str]:
    if not path.exists():
        atomic_write(path, block + "\n")
        return "created", path.name

    existing = read_preserving_newlines(path)
    newline = "\r\n" if "\r\n" in existing else "\n"
    normalized_block = block.replace("\n", newline)
    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL,
    )
    matches = list(pattern.finditer(existing))
    if len(matches) > 1:
        raise ValueError(
            f"AGENTS.md contains multiple managed blocks; resolve them manually: {path}"
        )
    if matches:
        updated = pattern.sub(lambda _: normalized_block, existing, count=1)
    else:
        separator = "" if not existing else (newline if existing.endswith(("\n", "\r")) else newline * 2)
        updated = existing + separator + normalized_block + newline
    if updated == existing:
        return "preserved", path.name
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(updated)
    return "updated", path.name


def write_guarded(
    path: Path,
    content: str,
    force: bool,
    relative_name: str,
) -> tuple[str, str]:
    existed = path.exists()
    if existed and not force:
        return "preserved", relative_name
    atomic_write(path, content)
    return ("updated" if existed else "created"), relative_name


def run_code_map(root: Path, skill_root: Path, skip: bool) -> dict[str, Any]:
    if skip:
        return {"action": "skipped"}
    script = skill_root / "scripts" / "code_map.py"
    action = "update" if (root / "docs/ai/code-map.json").exists() else "bootstrap"
    result = subprocess.run(
        [sys.executable, str(script), action, "--root", str(root), "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"Code-map {action} failed: {message}")
    try:
        details = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Code-map {action} returned invalid JSON") from exc
    return {"action": action, "details": details}


def initialize(args: argparse.Namespace) -> dict[str, Any]:
    root = normalize_root(args.root)
    brief_path, brief_text = resolve_brief(root, args.brief)
    values = collect_input(args, root, bool(brief_path))
    skill_root = Path(__file__).resolve().parents[1]
    policy = load_agents_policy(skill_root)

    result: dict[str, Any] = {
        "status": "initialized",
        "root": str(root),
        "created": [],
        "updated": [],
        "preserved": [],
    }
    operations = [
        write_guarded(
            root / "ProjectGoal.md",
            render_goal(values, brief_path, brief_text),
            args.force_goal,
            "ProjectGoal.md",
        ),
        write_guarded(
            root / "docs/ai/project-status.md",
            render_status(values, brief_path),
            args.force_status,
            "docs/ai/project-status.md",
        ),
        merge_agents(
            root / "AGENTS.md",
            render_managed_block(values, brief_path, policy),
        ),
    ]
    for action, relative_name in operations:
        result[action].append(relative_name)
    result["code_map"] = run_code_map(root, skill_root, args.no_code_map)
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Create or safely merge product goals, project status, AGENTS policy, "
            "and the repository code map."
        )
    )
    parser.add_argument("--root", default=".", help="Project root directory")
    parser.add_argument("--project-name", help="Product or project name")
    parser.add_argument("--target-users", help="Target users; separate items with semicolons")
    parser.add_argument("--outcome", help="Primary product outcome")
    parser.add_argument("--milestone", help="Current product milestone")
    parser.add_argument(
        "--success-criteria",
        help="Success criteria; separate items with semicolons",
    )
    parser.add_argument("--non-goals", help="Non-goals; separate items with semicolons")
    parser.add_argument("--constraints", help="Constraints; separate items with semicolons")
    parser.add_argument("--brief", help="UTF-8 business brief path")
    parser.add_argument(
        "--force-goal",
        action="store_true",
        help="Replace an existing ProjectGoal.md",
    )
    parser.add_argument(
        "--force-status",
        action="store_true",
        help="Replace an existing docs/ai/project-status.md",
    )
    parser.add_argument(
        "--no-code-map",
        action="store_true",
        help="Skip code-map bootstrap or update",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON only")
    return parser


def emit(result: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False))
        return
    print(f"Status: {result['status']}")
    print(f"Root: {result['root']}")
    for key in ("created", "updated", "preserved"):
        if result[key]:
            print(f"{key.title()}: {', '.join(result[key])}")
    print(f"Code map: {result['code_map']['action']}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = initialize(args)
        emit(result, args.json)
        return 0
    except (ValueError, OSError, RuntimeError) as exc:
        result = {"status": "error", "message": str(exc)}
        if args.json:
            print(json.dumps(result, ensure_ascii=False))
        else:
            print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

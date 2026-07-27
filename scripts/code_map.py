#!/usr/bin/env python3
"""Build and maintain a compact, deterministic repository code map."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = 1
MAP_JSON = Path("docs/ai/code-map.json")
MAP_MARKDOWN = Path("docs/ai/code-map.md")

IGNORED_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    ".next",
    ".nuxt",
    ".output",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "__pycache__",
    "node_modules",
    "vendor",
    "vendors",
    "dist",
    "build",
    "out",
    "target",
    "coverage",
    "generated",
    "tmp",
    "temp",
}

SOURCE_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".mjs",
    ".cjs",
    ".java",
    ".kt",
    ".kts",
    ".cs",
    ".go",
    ".rs",
    ".rb",
    ".php",
    ".swift",
    ".vue",
    ".svelte",
    ".c",
    ".cc",
    ".cpp",
    ".h",
    ".hpp",
    ".sql",
}

DOCUMENT_EXTENSIONS = {".md", ".mdx", ".rst", ".adoc"}

MANIFESTS = {
    "package.json": {"javascript"},
    "tsconfig.json": {"typescript"},
    "pyproject.toml": {"python"},
    "requirements.txt": {"python"},
    "setup.py": {"python"},
    "pom.xml": {"java"},
    "build.gradle": {"java"},
    "build.gradle.kts": {"kotlin"},
    "go.mod": {"go"},
    "Cargo.toml": {"rust"},
    "Gemfile": {"ruby"},
    "composer.json": {"php"},
    "Package.swift": {"swift"},
    "global.json": {"dotnet"},
}

EXTENSION_STACKS = {
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".py": "python",
    ".java": "java",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".cs": "dotnet",
    ".go": "go",
    ".rs": "rust",
    ".rb": "ruby",
    ".php": "php",
    ".swift": "swift",
    ".vue": "vue",
    ".svelte": "svelte",
    ".sql": "sql",
    ".c": "c-cpp",
    ".cc": "c-cpp",
    ".cpp": "c-cpp",
    ".h": "c-cpp",
    ".hpp": "c-cpp",
}

SEMANTIC_FIELDS = (
    "product_capability",
    "responsibility",
    "reuse_guidance",
    "notes",
    "needs_ai_review",
)

SEMANTIC_NODE_TYPES = {
    "module",
    "entry",
    "route",
    "component",
    "api",
    "service",
    "domain",
    "repository",
    "data_model",
    "integration",
    "job",
    "state",
}

TYPE_ORDER = (
    "entry",
    "module",
    "route",
    "component",
    "api",
    "service",
    "domain",
    "repository",
    "data_model",
    "integration",
    "job",
    "state",
    "test",
    "documentation",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_root(value: str) -> Path:
    root = Path(value).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Project root does not exist or is not a directory: {root}")
    return root


def run_git(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def git_metadata(root: Path) -> dict[str, Any]:
    head = run_git(root, "rev-parse", "HEAD")
    status = run_git(root, "status", "--porcelain")
    return {
        "source_head": head or None,
        "working_tree_dirty": bool(status),
    }


def is_ignored(relative: Path) -> bool:
    parts = {part.lower() for part in relative.parts}
    if parts & {name.lower() for name in IGNORED_DIRECTORIES}:
        return True
    normalized = relative.as_posix().lower()
    return normalized in {
        MAP_JSON.as_posix().lower(),
        MAP_MARKDOWN.as_posix().lower(),
    }


def discover_files(root: Path) -> list[Path]:
    files: list[Path] = []
    allowed = SOURCE_EXTENSIONS | DOCUMENT_EXTENSIONS
    manifest_names = {name.lower() for name in MANIFESTS}
    for current, directories, names in os.walk(root):
        current_path = Path(current)
        relative_dir = current_path.relative_to(root)
        directories[:] = [
            directory
            for directory in directories
            if not is_ignored(relative_dir / directory)
        ]
        for name in names:
            relative = (relative_dir / name) if relative_dir.parts else Path(name)
            if is_ignored(relative):
                continue
            if Path(name).suffix.lower() in allowed or name.lower() in manifest_names:
                files.append(relative)
    return sorted(files, key=lambda path: path.as_posix().lower())


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def detect_stacks(root: Path, files: Iterable[Path]) -> list[str]:
    stacks: set[str] = set()
    for relative in files:
        manifest_stack = MANIFESTS.get(relative.name)
        if manifest_stack:
            stacks.update(manifest_stack)
        stack = EXTENSION_STACKS.get(relative.suffix.lower())
        if stack:
            stacks.add(stack)
    package_path = root / "package.json"
    if package_path.exists():
        package_text = read_text(package_path).lower()
        for framework in ("react", "next", "vue", "svelte", "angular", "express", "nestjs"):
            if f'"{framework}"' in package_text or f'"@{framework}/' in package_text:
                stacks.add(framework)
    return sorted(stacks)


def slug(value: str) -> str:
    result = re.sub(r"[^a-zA-Z0-9]+", ".", value).strip(".").lower()
    return result or "root"


def without_source_suffix(relative: Path) -> str:
    value = relative.as_posix()
    suffixes = sorted(
        SOURCE_EXTENSIONS | DOCUMENT_EXTENSIONS,
        key=len,
        reverse=True,
    )
    lowered = value.lower()
    for suffix in suffixes:
        if lowered.endswith(suffix):
            return value[: -len(suffix)]
    return value


def file_node_id(relative: Path) -> str:
    return slug(without_source_suffix(relative))


def module_node_id(relative_directory: Path) -> str:
    return f"module.{slug(relative_directory.as_posix())}"


def is_test_path(relative: Path) -> bool:
    lowered_parts = [part.lower() for part in relative.parts]
    name = relative.name.lower()
    return (
        any(part in {"test", "tests", "__tests__", "spec", "specs", "e2e"} for part in lowered_parts)
        or ".test." in name
        or ".spec." in name
        or name.startswith("test_")
        or name.endswith("_test.py")
    )


def classify_file(relative: Path) -> str | None:
    suffix = relative.suffix.lower()
    if suffix in DOCUMENT_EXTENSIONS:
        return "documentation"
    if suffix not in SOURCE_EXTENSIONS:
        return None
    if is_test_path(relative):
        return "test"

    path_text = relative.as_posix().lower()
    stem = relative.stem.lower()
    parts = {part.lower() for part in relative.parts}

    if stem in {"index", "main", "app", "server", "cli", "program", "bootstrap"}:
        return "entry"
    if parts & {"routes", "router", "routers", "pages", "screens", "views"} or "route" in stem:
        return "route"
    if parts & {"components", "widgets"} or "component" in stem:
        return "component"
    if parts & {"controllers", "api", "endpoints"} or "controller" in stem:
        return "api"
    if parts & {"services", "usecases", "use-cases"} or "service" in stem or "usecase" in stem:
        return "service"
    if parts & {"repositories", "dao", "persistence"} or "repository" in stem:
        return "repository"
    if parts & {"integrations", "clients", "adapters", "gateways"} or any(
        token in stem for token in ("client", "adapter", "gateway")
    ):
        return "integration"
    if parts & {"jobs", "workers", "tasks", "consumers"} or any(
        token in stem for token in ("job", "worker", "consumer")
    ):
        return "job"
    if parts & {"store", "stores", "state"} or any(
        token in stem for token in ("store", "state", "reducer")
    ):
        return "state"
    if parts & {"domain", "entities", "aggregates"} or any(
        token in stem for token in ("entity", "aggregate", "value-object")
    ):
        return "domain"
    if parts & {"models", "schemas", "migrations"} or any(
        token in stem for token in ("model", "schema", "migration")
    ) or suffix == ".sql":
        return "data_model"
    if path_text.startswith(("src/", "app/", "lib/", "packages/", "apps/")):
        return None
    return None


def extract_python(text: str) -> tuple[list[str], list[str]]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return [], []
    symbols: list[str] = []
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith("_"):
                symbols.append(node.name)
        elif isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            prefix = "." * node.level
            imports.append(prefix + (node.module or ""))
    return sorted(set(symbols)), sorted(set(filter(None, imports)))


SYMBOL_PATTERN = re.compile(
    r"\b(?:export\s+)?(?:default\s+)?"
    r"(?:abstract\s+)?(?:class|interface|enum|function|type|const|struct|trait)\s+"
    r"([A-Za-z_][A-Za-z0-9_]*)"
)

IMPORT_PATTERNS = (
    re.compile(r"\bfrom\s*['\"]([^'\"]+)['\"]"),
    re.compile(r"\brequire\(\s*['\"]([^'\"]+)['\"]\s*\)"),
    re.compile(r"\bimport\(\s*['\"]([^'\"]+)['\"]\s*\)"),
    re.compile(r"^\s*import\s+(?:static\s+)?([A-Za-z_][A-Za-z0-9_.]*)\s*;", re.MULTILINE),
    re.compile(r"^\s*using\s+([A-Za-z_][A-Za-z0-9_.]*)\s*;", re.MULTILINE),
    re.compile(r"^\s*import\s+['\"]([^'\"]+)['\"]\s*;?\s*$", re.MULTILINE),
)


def extract_symbols_and_imports(path: Path, text: str) -> tuple[list[str], list[str]]:
    if path.suffix.lower() == ".py":
        return extract_python(text)
    symbols = sorted(set(SYMBOL_PATTERN.findall(text)))
    imports: set[str] = set()
    for pattern in IMPORT_PATTERNS:
        imports.update(pattern.findall(text))
    return symbols, sorted(imports)


def content_fingerprint(root: Path, paths: Iterable[str]) -> str:
    digest = hashlib.sha256()
    for relative_text in sorted(paths):
        relative = Path(relative_text)
        digest.update(relative.as_posix().encode("utf-8"))
        try:
            with (root / relative).open("rb") as handle:
                for chunk in iter(lambda: handle.read(65536), b""):
                    digest.update(chunk)
        except OSError:
            digest.update(b"<missing>")
    return f"sha256:{digest.hexdigest()}"


def source_module_directories(files: Iterable[Path]) -> dict[Path, list[Path]]:
    modules: dict[Path, list[Path]] = defaultdict(list)
    for relative in files:
        if relative.suffix.lower() not in SOURCE_EXTENSIONS or is_test_path(relative):
            continue
        parts = relative.parts
        if len(parts) == 1:
            directory = Path(".")
        else:
            depth = 2 if len(parts) > 2 else 1
            directory = Path(*parts[:depth])
        modules[directory].append(relative)
    return modules


def make_node(
    root: Path,
    node_id: str,
    node_type: str,
    name: str,
    paths: list[Path],
    symbols: list[str] | None = None,
    imports: list[str] | None = None,
) -> dict[str, Any]:
    path_strings = [path.as_posix() for path in sorted(paths)]
    return {
        "id": node_id,
        "type": node_type,
        "name": name,
        "paths": path_strings,
        "symbols": sorted(set(symbols or []))[:80],
        "imports": sorted(set(imports or []))[:200],
        "dependencies": [],
        "tests": [],
        "product_capability": "",
        "responsibility": "",
        "reuse_guidance": "",
        "notes": "",
        "fingerprint": content_fingerprint(root, path_strings),
        "needs_ai_review": node_type in SEMANTIC_NODE_TYPES,
        "last_verified": utc_now(),
    }


def candidate_paths(base: Path) -> list[Path]:
    candidates = [base]
    candidates.extend(Path(str(base) + extension) for extension in SOURCE_EXTENSIONS)
    candidates.extend(base / f"index{extension}" for extension in SOURCE_EXTENSIONS)
    return candidates


def resolve_import(
    source: Path,
    imported: str,
    file_to_node: dict[str, str],
) -> str | None:
    if not imported.startswith("."):
        return None
    if source.suffix.lower() == ".py":
        level = len(imported) - len(imported.lstrip("."))
        module = imported[level:]
        parent = source.parent
        for _ in range(max(0, level - 1)):
            parent = parent.parent
        base = parent / module.replace(".", "/") if module else parent / "__init__"
    else:
        base = Path(os.path.normpath(str(source.parent / imported)))
    for candidate in candidate_paths(base):
        key = candidate.as_posix().lower()
        if key in file_to_node:
            return file_to_node[key]
    return None


def preserve_semantics(
    current_nodes: list[dict[str, Any]],
    previous: dict[str, Any] | None,
) -> None:
    if not previous:
        return
    old_nodes = {node.get("id"): node for node in previous.get("nodes", [])}
    for node in current_nodes:
        old = old_nodes.get(node["id"])
        if not old:
            continue
        for field in SEMANTIC_FIELDS:
            if field in old:
                node[field] = old[field]


def build_map(root: Path, previous: dict[str, Any] | None = None) -> dict[str, Any]:
    files = discover_files(root)
    nodes: list[dict[str, Any]] = []
    file_to_node: dict[str, str] = {}

    for directory, module_files in source_module_directories(files).items():
        module_name = "root" if directory == Path(".") else directory.name
        nodes.append(
            make_node(
                root,
                module_node_id(directory),
                "module",
                module_name,
                module_files,
            )
        )

    file_details: dict[str, tuple[Path, list[str]]] = {}
    for relative in files:
        node_type = classify_file(relative)
        if not node_type:
            continue
        if node_type == "documentation":
            symbols, imports = [], []
        else:
            text = read_text(root / relative)
            symbols, imports = extract_symbols_and_imports(relative, text)
        node_id = file_node_id(relative)
        name = symbols[0] if symbols else relative.stem
        node = make_node(root, node_id, node_type, name, [relative], symbols, imports)
        nodes.append(node)
        file_to_node[relative.as_posix().lower()] = node_id
        file_details[node_id] = (relative, imports)

    nodes_by_id = {node["id"]: node for node in nodes}
    edges: list[dict[str, Any]] = []
    edge_keys: set[tuple[str, str, str]] = set()
    for node_id, (source, imports) in file_details.items():
        for imported in imports:
            target_id = resolve_import(source, imported, file_to_node)
            if not target_id or target_id == node_id:
                continue
            key = (node_id, target_id, "imports")
            if key in edge_keys:
                continue
            edge_keys.add(key)
            edges.append(
                {
                    "from": node_id,
                    "to": target_id,
                    "type": "imports",
                    "source": "script",
                    "verified": True,
                }
            )
            nodes_by_id[node_id]["dependencies"].append(target_id)
            if nodes_by_id[node_id]["type"] == "test":
                nodes_by_id[target_id]["tests"].extend(nodes_by_id[node_id]["paths"])

    preserve_semantics(nodes, previous)

    if previous:
        valid_ids = {node["id"] for node in nodes}
        for edge in previous.get("edges", []):
            if (
                edge.get("source") == "ai"
                and edge.get("verified") is True
                and edge.get("from") in valid_ids
                and edge.get("to") in valid_ids
            ):
                key = (edge["from"], edge["to"], edge.get("type", "related"))
                if key not in edge_keys:
                    edges.append(edge)
                    edge_keys.add(key)

    for node in nodes:
        node["dependencies"] = sorted(set(node["dependencies"]))
        node["tests"] = sorted(set(node["tests"]))

    metadata = {
        "schema_version": SCHEMA_VERSION,
        "project": root.name,
        "generated_at": utc_now(),
        "stacks": detect_stacks(root, files),
        "node_count": len(nodes),
        **git_metadata(root),
    }
    return {
        "meta": metadata,
        "nodes": sorted(nodes, key=lambda node: (node["type"], node["id"])),
        "edges": sorted(
            edges,
            key=lambda edge: (
                edge.get("from", ""),
                edge.get("to", ""),
                edge.get("type", ""),
            ),
        ),
    }


def load_map(root: Path) -> dict[str, Any]:
    path = root / MAP_JSON
    if not path.exists():
        raise FileNotFoundError(f"Code map does not exist: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read code map: {exc}") from exc
    if payload.get("meta", {}).get("schema_version") != SCHEMA_VERSION:
        raise ValueError(
            f"Unsupported code-map schema: {payload.get('meta', {}).get('schema_version')}"
        )
    if not isinstance(payload.get("nodes"), list) or not isinstance(payload.get("edges"), list):
        raise ValueError("Code map must contain nodes and edges arrays")
    return payload


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def save_json(root: Path, payload: dict[str, Any]) -> None:
    atomic_write(
        root / MAP_JSON,
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
    )


def render_markdown(payload: dict[str, Any]) -> str:
    meta = payload["meta"]
    lines = [
        "# Code Map",
        "",
        "> Generated structural facts. Source code remains authoritative.",
        "",
        "## Repository",
        "",
        f"- Project: `{meta.get('project', '')}`",
        f"- Generated: `{meta.get('generated_at', '')}`",
        f"- Source HEAD: `{meta.get('source_head') or 'not available'}`",
        f"- Working tree dirty: `{'yes' if meta.get('working_tree_dirty') else 'no'}`",
        f"- Stacks: `{', '.join(meta.get('stacks', [])) or 'not detected'}`",
        f"- Nodes: `{meta.get('node_count', len(payload.get('nodes', [])))}`",
        "",
        "Run `code_map.py check --root .` before coding and `update` after structural changes.",
        "",
    ]
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in payload.get("nodes", []):
        grouped[node.get("type", "other")].append(node)

    ordered_types = list(TYPE_ORDER)
    ordered_types.extend(sorted(set(grouped) - set(ordered_types)))
    for node_type in ordered_types:
        nodes = grouped.get(node_type, [])
        if not nodes:
            continue
        lines.extend([f"## {node_type.replace('_', ' ').title()}", ""])
        for node in sorted(nodes, key=lambda item: item["id"]):
            lines.append(f"### `{node['id']}` - {node.get('name', '')}")
            lines.append("")
            paths = node.get("paths", [])
            path_text = ", ".join(f"`{path}`" for path in paths[:12])
            if len(paths) > 12:
                path_text += f" (+{len(paths) - 12} more)"
            lines.append(f"- Paths: {path_text}")
            if node.get("product_capability"):
                lines.append(f"- Product capability: {node['product_capability']}")
            if node.get("responsibility"):
                lines.append(f"- Responsibility: {node['responsibility']}")
            if node.get("symbols"):
                lines.append(
                    "- Public symbols: "
                    + ", ".join(f"`{symbol}`" for symbol in node["symbols"][:12])
                )
            if node.get("dependencies"):
                lines.append(
                    "- Depends on: "
                    + ", ".join(f"`{item}`" for item in node["dependencies"][:12])
                )
            if node.get("tests"):
                lines.append(
                    "- Tests: " + ", ".join(f"`{item}`" for item in node["tests"][:12])
                )
            if node.get("reuse_guidance"):
                lines.append(f"- Reuse guidance: {node['reuse_guidance']}")
            if node.get("notes"):
                lines.append(f"- Notes: {node['notes']}")
            if node.get("needs_ai_review"):
                lines.append("- Semantic review: required")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def save_markdown(root: Path, payload: dict[str, Any]) -> None:
    atomic_write(root / MAP_MARKDOWN, render_markdown(payload))


def structural_snapshot(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    fields = (
        "type",
        "name",
        "paths",
        "symbols",
        "imports",
        "dependencies",
        "tests",
        "fingerprint",
    )
    return {
        node["id"]: {field: node.get(field) for field in fields}
        for node in payload.get("nodes", [])
    }


def compare_maps(
    stored: dict[str, Any],
    current: dict[str, Any],
) -> dict[str, list[str]]:
    old = structural_snapshot(stored)
    new = structural_snapshot(current)
    old_ids = set(old)
    new_ids = set(new)
    invalid_edges = []
    for edge in stored.get("edges", []):
        if edge.get("from") not in old_ids or edge.get("to") not in old_ids:
            invalid_edges.append(
                f"{edge.get('from', '?')}->{edge.get('to', '?')}:{edge.get('type', '?')}"
            )
    return {
        "added_nodes": sorted(new_ids - old_ids),
        "removed_nodes": sorted(old_ids - new_ids),
        "changed_nodes": sorted(
            node_id for node_id in old_ids & new_ids if old[node_id] != new[node_id]
        ),
        "invalid_edges": sorted(invalid_edges),
        "pending_ai_review": sorted(
            node["id"]
            for node in stored.get("nodes", [])
            if node.get("needs_ai_review")
        ),
    }


def summary(
    status: str,
    root: Path,
    payload: dict[str, Any] | None = None,
    comparison: dict[str, list[str]] | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "status": status,
        "root": str(root),
        "map_json": str(root / MAP_JSON),
        "map_markdown": str(root / MAP_MARKDOWN),
    }
    if payload:
        result["node_count"] = len(payload.get("nodes", []))
        result["stacks"] = payload.get("meta", {}).get("stacks", [])
    if comparison:
        result.update(comparison)
    return result


def emit(payload: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False))
        return
    print(f"Status: {payload['status']}")
    print(f"Root: {payload['root']}")
    if "node_count" in payload:
        print(f"Nodes: {payload['node_count']}")
    for key in ("added_nodes", "removed_nodes", "changed_nodes", "invalid_edges"):
        values = payload.get(key, [])
        if values:
            print(f"{key.replace('_', ' ').title()}: {', '.join(values)}")
    pending = payload.get("pending_ai_review", [])
    if pending:
        print(f"Pending AI semantic review: {len(pending)}")


def command_bootstrap(root: Path, force: bool) -> dict[str, Any]:
    map_path = root / MAP_JSON
    if map_path.exists() and not force:
        raise ValueError(f"Code map already exists; use update or bootstrap --force: {map_path}")
    payload = build_map(root)
    save_json(root, payload)
    save_markdown(root, payload)
    return summary("created", root, payload)


def command_check(root: Path) -> tuple[dict[str, Any], int]:
    try:
        stored = load_map(root)
    except FileNotFoundError:
        return summary("missing", root), 1
    current = build_map(root, stored)
    comparison = compare_maps(stored, current)
    stale_keys = ("added_nodes", "removed_nodes", "changed_nodes", "invalid_edges")
    is_stale = any(comparison[key] for key in stale_keys)
    return summary("stale" if is_stale else "fresh", root, stored, comparison), int(is_stale)


def command_update(root: Path) -> dict[str, Any]:
    try:
        stored = load_map(root)
    except FileNotFoundError:
        payload = build_map(root)
        comparison = {
            "added_nodes": [node["id"] for node in payload["nodes"]],
            "removed_nodes": [],
            "changed_nodes": [],
            "invalid_edges": [],
            "pending_ai_review": [
                node["id"] for node in payload["nodes"] if node.get("needs_ai_review")
            ],
        }
    else:
        payload = build_map(root, stored)
        comparison = compare_maps(stored, payload)
    save_json(root, payload)
    save_markdown(root, payload)
    return summary("updated", root, payload, comparison)


def command_render(root: Path) -> dict[str, Any]:
    payload = load_map(root)
    save_markdown(root, payload)
    return summary("rendered", root, payload)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build and maintain docs/ai/code-map.json and code-map.md."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("bootstrap", "check", "update", "render"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--root", default=".", help="Project root directory")
        subparser.add_argument(
            "--json",
            action="store_true",
            help="Emit a machine-readable command summary",
        )
        if command == "bootstrap":
            subparser.add_argument(
                "--force",
                action="store_true",
                help="Replace an existing map",
            )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        root = normalize_root(args.root)
        if args.command == "bootstrap":
            result = command_bootstrap(root, args.force)
            exit_code = 0
        elif args.command == "check":
            result, exit_code = command_check(root)
        elif args.command == "update":
            result = command_update(root)
            exit_code = 0
        else:
            result = command_render(root)
            exit_code = 0
        emit(result, args.json)
        return exit_code
    except (FileNotFoundError, ValueError, OSError) as exc:
        error = {
            "status": "error",
            "message": str(exc),
        }
        if getattr(args, "json", False):
            print(json.dumps(error, ensure_ascii=False))
        else:
            print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

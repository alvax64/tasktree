#!/usr/bin/env python3
"""Lint Markdown tasktree files for common coordination errors."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


TASK_RE = re.compile(
    r"^(?P<prefix>[\s│|]*(?:├──|└──|\+-|-|\*)\s+)?"
    r"\[(?P<status>[^\]]*)\]\s+"
    r"(?P<task_id>[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)?(?:-\d+)?(?:\.\d+)*)\b"
    r"(?P<rest>.*)$"
)
CONFLICT_RE = re.compile(r"^(<<<<<<<|=======|>>>>>>>)")
LINK_RE = re.compile(r"(?:->|\u2192)\s+(?P<path>[^#{}\n]+)")

DEFAULT_STATUSES = {"[ ]", "[x]", "[I]", "[B]", "[Q]", "[R]", "[H]", "[?]", "[!]"}
DETAIL_DIR_NAMES = {"details", "detail"}


@dataclass
class Finding:
    path: Path
    line: int
    message: str
    severity: str = "error"

    def format(self, root: Path) -> str:
        try:
            display = self.path.relative_to(root)
        except ValueError:
            display = self.path
        return f"{display}:{self.line}: {self.severity}: {self.message}"

    def as_json(self, root: Path) -> dict[str, object]:
        try:
            display = self.path.relative_to(root)
        except ValueError:
            display = self.path
        return {
            "path": str(display),
            "line": self.line,
            "severity": self.severity,
            "message": self.message,
        }


def normalize_status(raw: str) -> str | None:
    if raw == " ":
        return "[ ]"
    if raw == "x":
        return "[x]"
    if len(raw) == 1 and raw.strip() == raw:
        return f"[{raw}]"
    return None


def tasktree_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    files = set(root.glob("TASKTREE.md"))
    files.update(root.glob("**/*TASKTREE.md"))
    files.update(root.glob("**/TASKTREE.md"))
    return sorted(path for path in files if path.is_file())


def load_statuses(root: Path) -> set[str]:
    statuses = set(DEFAULT_STATUSES)
    candidates = []
    if root.is_file():
        candidates.append(root.parent / "status-legend.md")
    else:
        candidates.extend(root.glob("status-legend.md"))
        candidates.extend(root.glob("**/status-legend.md"))

    for path in candidates:
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            match = re.match(r"^\[(?P<status>[^\]]*)\]\s+", line)
            if match:
                normalized = normalize_status(match.group("status"))
                if normalized:
                    statuses.add(normalized)
    return statuses


def lint_file(
    path: Path,
    root: Path,
    ids: dict[str, tuple[Path, int]],
    statuses: set[str],
    linked_details: set[Path],
) -> list[Finding]:
    findings: list[Finding] = []
    text = path.read_text(encoding="utf-8")

    for number, line in enumerate(text.splitlines(), start=1):
        if CONFLICT_RE.match(line):
            findings.append(Finding(path, number, "unresolved Git conflict marker"))

        match = TASK_RE.match(line)
        if not match:
            continue

        status = normalize_status(match.group("status"))
        if status is None:
            findings.append(Finding(path, number, "malformed status marker"))
        elif status not in DEFAULT_STATUSES:
            if status not in statuses:
                findings.append(Finding(path, number, f"unknown status {status}; add it to status-legend.md"))

        task_id = match.group("task_id")
        if task_id in ids:
            first_path, first_line = ids[task_id]
            findings.append(
                Finding(path, number, f"duplicate task id {task_id}; first seen at {first_path}:{first_line}")
            )
        else:
            ids[task_id] = (path, number)

        link_match = LINK_RE.search(match.group("rest"))
        if link_match:
            raw_path = link_match.group("path").strip()
            target = raw_path.split()[0].rstrip(".,")
            if not re.match(r"^[a-z]+://", target):
                resolved = (path.parent / target).resolve()
                if not resolved.exists():
                    findings.append(Finding(path, number, f"linked detail path does not exist: {target}"))
                else:
                    linked_details.add(resolved)

    return findings


def task_ids_from_file(path: Path) -> set[str]:
    ids = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = TASK_RE.match(line)
        if match:
            ids.add(match.group("task_id"))
    return ids


def lint_next_recommended(path: Path, known_ids: set[str]) -> list[Finding]:
    findings: list[Finding] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    in_section = False
    for number, line in enumerate(lines, start=1):
        if line.startswith("## "):
            in_section = line.strip().lower() == "## next recommended task"
            continue
        if not in_section or not line.strip().startswith("-"):
            continue
        match = re.search(r"\b([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)?(?:-\d+)?(?:\.\d+)*)\b", line)
        if match and match.group(1) not in known_ids and match.group(1).lower() != "none":
            findings.append(Finding(path, number, f"Next Recommended Task references unknown task id {match.group(1)}"))
    return findings


def lint_dangling_details(root: Path, linked_details: set[Path]) -> list[Finding]:
    findings: list[Finding] = []
    base = root if root.is_dir() else root.parent
    for directory in DETAIL_DIR_NAMES:
        details_root = base / directory
        if not details_root.is_dir():
            continue
        for path in sorted(details_root.glob("**/*.md")):
            resolved = path.resolve()
            if resolved not in linked_details:
                findings.append(Finding(path, 1, "detail file is not linked from a tasktree task", "warning"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint Markdown tasktree files.")
    parser.add_argument("root", nargs="?", default=".tasktree", help="Tasktree root directory or file")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON output")
    parser.add_argument("--strict", action="store_true", help="Enable additional consistency checks")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"tasktree_lint: path does not exist: {root}", file=sys.stderr)
        return 2

    files = tasktree_files(root)
    if not files:
        print(f"tasktree_lint: no TASKTREE.md files found under {root}", file=sys.stderr)
        return 2

    display_root = root if root.is_dir() else root.parent
    statuses = load_statuses(root)
    ids: dict[str, tuple[Path, int]] = {}
    linked_details: set[Path] = set()
    findings: list[Finding] = []
    for path in files:
        findings.extend(lint_file(path, display_root, ids, statuses, linked_details))

    if args.strict:
        known_ids = set(ids)
        for path in files:
            findings.extend(lint_next_recommended(path, known_ids))
        findings.extend(lint_dangling_details(root, linked_details))

    if args.json:
        print(json.dumps({
            "ok": not any(f.severity == "error" for f in findings),
            "files": len(files),
            "findings": [finding.as_json(display_root) for finding in findings],
        }, indent=2))
        return 1 if any(f.severity == "error" for f in findings) else 0

    if findings:
        for finding in findings:
            print(finding.format(display_root))
        return 1 if any(f.severity == "error" for f in findings) else 0

    print(f"tasktree_lint: OK ({len(files)} file(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

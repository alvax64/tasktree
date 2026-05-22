#!/usr/bin/env python3
"""Lint Markdown tasktree files for common coordination errors."""

from __future__ import annotations

import argparse
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


@dataclass
class Finding:
    path: Path
    line: int
    message: str

    def format(self, root: Path) -> str:
        try:
            display = self.path.relative_to(root)
        except ValueError:
            display = self.path
        return f"{display}:{self.line}: {self.message}"


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


def lint_file(path: Path, root: Path, ids: dict[str, tuple[Path, int]]) -> list[Finding]:
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

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint Markdown tasktree files.")
    parser.add_argument("root", nargs="?", default=".tasktree", help="Tasktree root directory or file")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"tasktree_lint: path does not exist: {root}", file=sys.stderr)
        return 2

    files = tasktree_files(root)
    if not files:
        print(f"tasktree_lint: no TASKTREE.md files found under {root}", file=sys.stderr)
        return 2

    ids: dict[str, tuple[Path, int]] = {}
    findings: list[Finding] = []
    for path in files:
        findings.extend(lint_file(path, root if root.is_dir() else root.parent, ids))

    if findings:
        display_root = root if root.is_dir() else root.parent
        for finding in findings:
            print(finding.format(display_root))
        return 1

    print(f"tasktree_lint: OK ({len(files)} file(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

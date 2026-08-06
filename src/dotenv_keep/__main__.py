"""Command-line interface for dotenv-keep."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import compare, find_references, load

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__"}
CODE_SUFFIXES = {".py", ".js", ".ts", ".go"}


def scan_references(directory: Path) -> set[str]:
    """Collect referenced variable names from source files under directory."""
    refs: set[str] = set()
    for path in directory.rglob("*"):
        if path.is_dir() or path.name in SKIP_DIRS:
            continue
        if path.suffix not in CODE_SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        refs |= find_references(path.read_text(encoding="utf-8", errors="ignore"))
    return refs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="dotenv-keep",
        description="Keep environment variable names in sync across repos.",
    )
    parser.add_argument(
        "--example",
        default=".env.example",
        help="example env file (default: .env.example)",
    )
    parser.add_argument(
        "--path",
        default=".",
        help="source directory to scan for references (default: .)",
    )
    args = parser.parse_args(argv)

    try:
        example = load(args.example)
    except OSError as exc:
        parser.error(f"cannot read {args.example}: {exc}")

    refs = scan_references(Path(args.path))
    missing, unused = compare(example, refs)

    for name in sorted(missing):
        print(f"missing: {name} is referenced in code but not in {args.example}")
    for name in sorted(unused):
        print(f"unused: {name} is in {args.example} but not referenced in code")

    if missing:
        return 1
    if unused:
        print(
            f"ok: {len(refs)} referenced variable(s) present; "
            f"{len(unused)} unused name(s) in {args.example}"
        )
        return 0
    print(f"ok: {len(refs)} referenced variable(s) present in {args.example}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Keep and manage .env files safely."""

from __future__ import annotations

import os
import re

KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
REF_RE = re.compile(
    r"(?:"
    r"os\.environ\s*[\[\(]?\s*['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]\s*[\]\)]?"
    r"|os\.getenv\s*\(\s*['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]\s*\)"
    r"|process\.env\.([A-Za-z_][A-Za-z0-9_]*)"
    r")"
)


def parse_line(line: str) -> tuple[str, str] | None:
    """Parse a single dotenv-style line into (key, value), or None to skip."""
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if line.startswith("export "):
        line = line[len("export ") :]
    if "=" not in line:
        return None
    key, _, value = line.partition("=")
    key = key.strip()
    value = value.strip()
    if (
        value.startswith('"') and value.endswith('"')
    ) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]
    elif "#" in value:
        value = value.split("#", 1)[0].rstrip()
    if not KEY_RE.match(key):
        return None
    return key, value


def parse_env(text: str) -> dict[str, str]:
    """Parse dotenv-style text into a mapping of names to values."""
    env: dict[str, str] = {}
    for line in text.splitlines():
        entry = parse_line(line)
        if entry is not None:
            key, value = entry
            env[key] = value
    return env


def load(path: str | os.PathLike[str]) -> dict[str, str]:
    """Load a .env file into a mapping of names to values."""
    with open(path, encoding="utf-8") as fh:
        return parse_env(fh.read())


def find_references(text: str) -> set[str]:
    """Find environment variable names referenced in source code."""
    refs: set[str] = set()
    for match in REF_RE.finditer(text):
        for group in match.groups():
            if group is not None:
                refs.add(group)
    return refs


def compare(example: dict[str, str], code_refs: set[str]) -> tuple[set[str], set[str]]:
    """Return (missing, unused) variable names.

    Missing: referenced in code but absent from the example file.
    Unused: present in the example file but not referenced in code.
    """
    example_keys = set(example)
    missing = code_refs - example_keys
    unused = example_keys - code_refs
    return missing, unused

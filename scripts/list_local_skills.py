#!/usr/bin/env python3
"""List local Codex skill metadata for routing."""

import argparse
import json
import os
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


DEFAULT_ROOTS = [
    Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills",
    Path.home() / ".agents" / "skills",
    Path.home() / ".codex" / "plugins" / "cache",
]


def parse_frontmatter(skill_md):
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    raw = text[4:end]
    if yaml is not None:
        data = yaml.safe_load(raw)
        return data if isinstance(data, dict) else None

    data = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data


def iter_skill_files(roots):
    seen = set()
    for root in roots:
        root = root.expanduser()
        if not root.exists():
            continue
        for path in root.rglob("SKILL.md"):
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            yield resolved


def collect_skills(roots):
    skills = []
    for skill_md in iter_skill_files(roots):
        metadata = parse_frontmatter(skill_md) or {}
        name = metadata.get("name")
        description = metadata.get("description")
        if not isinstance(name, str) or not name.strip():
            name = skill_md.parent.name
        if not isinstance(description, str):
            description = ""
        skills.append(
            {
                "name": name.strip(),
                "description": " ".join(description.split()),
                "path": str(skill_md),
                "directory": str(skill_md.parent),
            }
        )
    return sorted(skills, key=lambda item: (item["name"], item["path"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    parser.add_argument(
        "--root",
        action="append",
        default=[],
        help="Additional root directory to search. Repeat as needed.",
    )
    args = parser.parse_args()

    roots = DEFAULT_ROOTS + [Path(root) for root in args.root]
    skills = collect_skills(roots)

    if args.json:
        print(json.dumps(skills, ensure_ascii=False, indent=2))
        return

    for skill in skills:
        print(f"{skill['name']}\t{skill['path']}")
        if skill["description"]:
            print(f"  {skill['description']}")


if __name__ == "__main__":
    main()

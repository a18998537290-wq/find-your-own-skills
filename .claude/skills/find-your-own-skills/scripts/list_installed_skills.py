#!/usr/bin/env python3
"""List installed Claude skills and rank them against a query."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path


STOPWORDS = {
    "a",
    "an",
    "and",
    "for",
    "from",
    "help",
    "i",
    "in",
    "is",
    "me",
    "of",
    "the",
    "to",
    "use",
    "want",
    "with",
    "我",
    "想",
    "帮",
    "帮我",
    "一个",
    "的",
    "了",
}


def skill_roots():
    roots = []
    cwd = Path.cwd().resolve()
    for current in [cwd, *cwd.parents]:
        candidate = current / ".claude" / "skills"
        if candidate.exists():
            roots.append(candidate)
    personal = Path.home() / ".claude" / "skills"
    if personal.exists():
        roots.append(personal)
    seen = set()
    ordered = []
    for root in roots:
        resolved = root.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        ordered.append(resolved)
    return ordered


def parse_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 4 :].lstrip("\n")
    data = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data, body


def summarize_body(body: str) -> str:
    summary_lines = []
    in_code = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not stripped:
            if summary_lines:
                break
            continue
        if stripped.startswith("#"):
            continue
        summary_lines.append(stripped)
        if len(" ".join(summary_lines)) >= 220:
            break
    return " ".join(" ".join(summary_lines).split())[:240]


def tokenize(text: str):
    return [token for token in re.split(r"[^a-z0-9\u4e00-\u9fff]+", text.lower()) if token and token not in STOPWORDS]


def score_skill(skill: dict, query_tokens: list[str]):
    if not query_tokens:
        return 0, []
    name_tokens = set(tokenize(skill["name"]))
    haystack_text = " ".join(
        [
            skill["name"],
            skill["description"],
            skill.get("when_to_use", ""),
            skill["summary"],
            skill["path"],
        ]
    )
    haystack_tokens = tokenize(haystack_text)
    haystack_counts = {token: haystack_tokens.count(token) for token in set(haystack_tokens)}
    score = 0
    matches = []
    for token in query_tokens:
        token_hits = haystack_counts.get(token, 0)
        if token_hits:
            matches.append(token)
            score += token_hits * (4 if token in name_tokens else 1)
    if skill["path"].startswith(str(Path.home() / ".claude" / "skills")):
        score += 1
    return score, sorted(set(matches))


def collect_skills(query: str):
    skills = []
    seen = set()
    query_tokens = tokenize(query)
    for root in skill_roots():
        for skill_md in root.rglob("SKILL.md"):
            if any(part.startswith(".") for part in skill_md.relative_to(root).parts[:-1]):
                continue
            resolved = skill_md.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            frontmatter, body = parse_frontmatter(skill_md)
            name = frontmatter.get("name") or skill_md.parent.name
            description = frontmatter.get("description", "")
            when_to_use = frontmatter.get("when_to_use", "")
            summary = summarize_body(body)
            skill = {
                "name": str(name).strip(),
                "description": " ".join(str(description).split()),
                "when_to_use": " ".join(str(when_to_use).split()),
                "summary": summary,
                "path": str(skill_md),
            }
            score, matches = score_skill(skill, query_tokens)
            skill["score"] = score
            skill["matches"] = matches
            skills.append(skill)

    skills = [skill for skill in skills if skill["name"].lower() != "find-your-own-skills"]
    if query_tokens:
        skills = [
            skill
            for skill in skills
            if skill["score"] >= 2 or len(skill["matches"]) >= 2
        ]
    skills.sort(key=lambda item: (-item["score"], item["name"].lower(), item["path"]))
    return skills


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", default="", help="User request text")
    parser.add_argument("--limit", type=int, default=5, help="Maximum matches to return")
    args = parser.parse_args()

    skills = collect_skills(args.query)
    top = skills[: max(1, args.limit)]
    print(json.dumps(top, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

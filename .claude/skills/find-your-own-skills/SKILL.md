---
name: find-your-own-skills
description: Help Claude Code or Claude Desktop find the best matching installed skill. Use when the user asks to search installed Claude skills, show ranked matches with detailed function summaries, and let the user choose one before loading it.
allowed-tools: Bash(python3 *) Bash(find *) Bash(cat *) Bash(rg *)
---

# Find Your Own Skills

## Goal

Search only installed Claude skills and route the request to the best match after the user chooses.

## Workflow

1. Read the user's request after `/find-your-own-skills` or the equivalent natural-language trigger.
2. Load the installed-skill inventory:

   !`python3 "${CLAUDE_SKILL_DIR}/scripts/list_installed_skills.py" --query "$ARGUMENTS"`

3. Show the top matches as a numbered list.
4. For each match, include:
   - skill name
   - why it matches
   - a short functional summary
   - the file path
5. Ask the user to choose one skill by name or number.
6. After the user chooses, open that skill's `SKILL.md` completely and follow its instructions.
7. If no local skill fits, say that clearly and continue with the best general Claude approach.

## Matching Rules

- Search only installed local Claude skills.
- Prefer user-installed skills over bundled or plugin skills.
- Rank by semantic fit, then by explicit name matches.
- Keep the response concise: at most five matches unless the user asks for more.

## Response Format

```text
找到这些已安装 skills：
1. skill-name - why it matches
   功能介绍：...
   路径：/absolute/path/to/SKILL.md

请选择要使用的 skill 名称或序号。
```

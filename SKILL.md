---
name: find-your-own-skills
description: Discover and route a user's requested capability to the best matching local Codex skill or plugin skill. Use when the user explicitly invokes "Find your own skills", "find your own skills", "$find-your-own-skills", "帮我找/匹配/使用合适的 skill", or describes a desired function after this skill and expects Codex to search the user's own skill/plugin library, choose the closest skill by meaning and capability, load that skill's instructions, and then perform the requested task with it.
---

# Find Your Own Skills

## Workflow

Use this skill as a router, not as the final domain expert.

1. Parse the user's actual requested capability from the text after the invocation.
2. Inventory local skills before deciding. Prefer the bundled script:

   ```bash
   python3 /Users/l/.codex/skills/find-your-own-skills/scripts/list_local_skills.py --json
   ```

   If the script is unavailable, search for `SKILL.md` under:
   - `${CODEX_HOME:-$HOME/.codex}/skills`
   - `$HOME/.agents/skills`
   - `$HOME/.codex/plugins/cache`

3. Match by semantic fit using each skill's `name`, `description`, and path. Prioritize:
   - explicitly named skills from the user
   - exact domain or artifact matches
   - required tool/plugin matches
   - workflow fit over keyword coincidence

4. If one skill is clearly best, announce it in one short line, open and read that skill's `SKILL.md` completely, follow its instructions, and complete the user's task.
5. If multiple skills are relevant, use the smallest set that covers the task and state the order. Read each selected `SKILL.md` before acting.
6. If no suitable local skill exists, say that briefly and continue with the best general Codex approach. If installing or creating a skill would be useful, suggest it only after handling what can be handled now.

## Matching Guidance

Treat skill descriptions as the trigger source of truth. The body of a candidate skill should be read only after selection, unless the metadata is ambiguous and reading one or two candidates is necessary to decide.

Prefer local/user skills over bundled or system skills when the fit is comparable. Prefer plugin skills when the user names a plugin or the task requires that plugin's UI/tool integration.

Do not delegate the entire decision to subagents. This skill is meant to help the current Codex instance choose and then use the right local capability.

## Examples

- User: "Use Find your own skills to deploy this app."
  Action: match `vercel-deploy` if available, read it, then deploy according to its instructions.
- User: "Find your own skills 帮我把论文做成中文组会 PPT."
  Action: match `nature-paper2ppt`, read it, then build the deck.
- User: "用 find-your-own-skills 找一个能控制浏览器截图的 skill."
  Action: match the Browser control skill, read it, then operate the browser.

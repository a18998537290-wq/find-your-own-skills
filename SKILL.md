---
name: find-your-own-skills
description: Discover and route a user's requested capability to the best matching installed Codex skill. Use when the user explicitly invokes "Find your own skills", "find your own skills", "$find-your-own-skills", "帮我找/匹配/使用合适的 skill", or describes a desired function after this skill and expects Codex to search only installed local skills, show ranked matches with detailed descriptions, let the user choose one, then load that skill's instructions and continue.
---

# Find Your Own Skills

## Workflow

Use this skill as a router, not as the final domain expert.

1. Parse the user's actual requested capability from the text after the invocation.
2. Inventory only installed local skills. Prefer the bundled script:

   ```bash
   python3 /Users/l/.codex/skills/find-your-own-skills/scripts/list_local_skills.py --json
   ```

   If the script is unavailable, search for `SKILL.md` only under:
   - `${CODEX_HOME:-$HOME/.codex}/skills`
   - `$HOME/.agents/skills`

   Ignore plugin caches and hidden/system skill directories such as `.system` unless the user explicitly asks to include them.

3. Match by semantic fit using each skill's `name`, `description`, and path. Prioritize:
   - explicitly named skills from the user
   - exact domain or artifact matches
   - required tool or workflow matches
   - workflow fit over keyword coincidence

4. Show the top matches first, with each candidate's detailed functional summary.
5. Ask the user to choose one candidate when the best match is not obvious, or when several are plausibly relevant.
6. After the user chooses, open and read that skill's `SKILL.md` completely, follow its instructions, and complete the user's task.
7. If no suitable local skill exists, say that briefly and continue with the best general Codex approach. If installing or creating a skill would be useful, suggest it only after handling what can be handled now.

## Response Format

When presenting matches, keep the list concise and useful:

```text
找到这些已安装 skills：
1. skill-name - why it matches
   功能介绍：what this skill can do, based on its metadata and summary.
   路径：/absolute/path/to/SKILL.md

请选择要使用的 skill 名称或序号。
```

Show at most five matches unless the user asks for more. If there is one obvious best match, still show it and ask for confirmation before loading and using it.

## Matching Guidance

Treat skill descriptions as the trigger source of truth. The body of a candidate skill should be read only after the user chooses, unless the metadata is too thin and reading one or two candidates is necessary to produce a meaningful description.

Prefer user-installed skills. Do not include plugin-cache skills or hidden/system skills in the candidate list unless the user explicitly expands the scope.

Do not delegate the entire decision to subagents. This skill is meant to help the current Codex instance choose and then use the right installed local capability.

## Examples

- User: "Use Find your own skills to deploy this app."
  Action: show local deployment-related skills, summarize them, ask the user to choose, then read the chosen one and deploy.
- User: "Find your own skills 帮我把论文做成中文组会 PPT."
  Action: show local presentation-related skills, summarize them, ask the user to choose, then read the chosen one and build the deck.
- User: "用 find-your-own-skills 找一个能控制浏览器截图的 skill."
  Action: show local browser-related skills, summarize them, ask the user to choose, then read the chosen one and operate the browser.

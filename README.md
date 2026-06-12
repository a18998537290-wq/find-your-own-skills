# Find Your Own Skills

> A tiny router skill that helps Codex and Claude find the right installed skill before doing the work.
>
> 一个“先找技能、再选技能、最后执行”的轻量路由 Skill，适用于 Codex 和 Claude。

[![Codex Skill](https://img.shields.io/badge/Codex-skill-111827)](#codex-usage)
[![Claude Skill](https://img.shields.io/badge/Claude-skill-6B46C1)](#claude-usage)
[![Bilingual](https://img.shields.io/badge/README-English%20%7C%20中文-blue)](#中文说明)

## Why Star / Watch?

- Star this repo if you use multiple AI-agent skills and want a cleaner way to choose the right one.
- Watch releases if you want updates for better matching, more agent formats, and improved install docs.

## 中文说明

当你的本地 skills 越来越多时，真正麻烦的不是“没有工具”，而是“不知道该用哪个工具”。`find-your-own-skills` 会先搜索已安装的本地 skills，展示匹配结果、功能简介和路径，让你选择一个，再加载并使用它。

仓库包含两个版本：

| 平台 | 文件位置 | 用途 |
| --- | --- | --- |
| Codex | `SKILL.md` | 在 Codex 中匹配并路由到本地已安装 skills |
| Claude Code / Claude Desktop | `.claude/skills/find-your-own-skills/SKILL.md` | 在 Claude 中匹配并路由到本地已安装 skills |

### 功能

- 只搜索已安装的本地 skills
- 展示最多 5 个匹配结果
- 给每个 skill 展示功能简介和路径
- 让用户选择后再读取目标 skill
- 同时支持 Codex 和 Claude 目录结构

### Codex 用法

把仓库内容放到你的 Codex skills 目录中，例如：

```bash
git clone https://github.com/a18998537290-wq/find-your-own-skills.git ~/.codex/skills/find-your-own-skills
```

然后在 Codex 中使用：

```text
$find-your-own-skills 帮我找一个能把论文做成中文 PPT 的 skill
```

### Claude 用法

把 Claude 版本复制或保留在项目的 `.claude/skills` 目录中：

```bash
mkdir -p .claude/skills
cp -R find-your-own-skills/.claude/skills/find-your-own-skills .claude/skills/
```

然后在 Claude Code / Claude Desktop 中使用自然语言触发：

```text
Use find-your-own-skills to find a skill for creating a presentation.
```

## English

When you have many local skills installed, the hard part is often not "do I have a tool?" but "which tool should I use?" `find-your-own-skills` searches installed local skills, shows matching candidates with short function summaries and paths, asks you to choose, then loads the selected skill.

This repository includes two versions:

| Platform | Location | Purpose |
| --- | --- | --- |
| Codex | `SKILL.md` | Match and route to installed local Codex skills |
| Claude Code / Claude Desktop | `.claude/skills/find-your-own-skills/SKILL.md` | Match and route to installed local Claude skills |

### Features

- Searches installed local skills only
- Shows up to 5 ranked matches
- Includes a short function summary and path for each match
- Waits for the user to choose before loading the target skill
- Supports both Codex and Claude skill layouts

### Codex Usage

Install into your Codex skills directory:

```bash
git clone https://github.com/a18998537290-wq/find-your-own-skills.git ~/.codex/skills/find-your-own-skills
```

Then use:

```text
$find-your-own-skills find a skill for deploying this app
```

### Claude Usage

Copy the Claude version into a project `.claude/skills` directory:

```bash
mkdir -p .claude/skills
cp -R find-your-own-skills/.claude/skills/find-your-own-skills .claude/skills/
```

Then ask Claude:

```text
Use find-your-own-skills to find a skill for creating a presentation.
```

## Contributing / 参与贡献

Issues and pull requests are welcome. Useful contributions include better matching rules, clearer docs, new agent-specific adapters, and real-world examples.

欢迎提交 issue 和 PR。尤其欢迎改进匹配规则、补充安装文档、增加更多 agent 适配版本，以及提供真实使用案例。

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

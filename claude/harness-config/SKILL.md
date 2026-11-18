---
name: harness-config
description: "Use when a skill names harness-config, or when changing Claude Code's own settings,
  hooks, CLAUDE.md, skills or plugins, choosing where a Claude skill is deployed, or bootstrapping
  a repository CLAUDE.md. Claude Code binding for edit-config, create-skill and repo guidance."
metadata:
  type: guideline
---

# Ownership

- `~/.claude/settings.json`, `~/.claude/CLAUDE.md` and owned personal skills can be chezmoi
  targets. Native `/update-config` or `/config` is not an ownership override: persistent managed
  changes go through the resolved source and edit-config's lifecycle, not a second write to the
  live destination.
- Skills installed from QStack are symlinks into a QStack clone. Resolve an installed skill's
  symlink to find it, and edit the skill in that repository, not through the link's parent
  directory and not in chezmoi.
- `~/.claude.json` holds runtime/auth/MCP state; use supported Claude MCP/settings commands for it.
- Never adopt `~/.claude/plugins/cache`, transcripts, credentials or generated installed-plugin
  registries. Plugin managers own fetched plugins and skill caches.
- Changes to skills or hooks are checked in a fresh Claude session; T3 injects its own MCP tools
  and settings. There is no Pi-style profile selector.

# Settings semantics

- For settings JSON, load native `/update-config` through `Skill` when exposed: it owns current
  settings, permissions and hook semantics. Give it the exact authoritative source path and a
  source-only editing boundary. If it is absent, consult the installed schema/docs and state the
  limitation rather than install a replacement.

# Skill loading

- Skills load as `<name>/SKILL.md` from a personal (`~/.claude/skills`), project (`.claude/skills`)
  or plugin root; T3 loads the same roots through the SDK. Verify actual discovery in a fresh
  session before advertising a skill.
- A nested child `SKILL.md` is not independently advertised; keep children on explicit parent
  routes with relative paths.
- `disable-model-invocation`, `user-invocable`, `context: fork`, `agent` and tool permissions have
  distinct Claude-specific semantics. A fork changes context and lifecycle, not just format.

# Guidance bootstrap

- For an explicitly requested new `CLAUDE.md`, native `/init` through `Skill` owns the initial
  codebase survey and draft when it is exposed and its destination and writing effects match the
  assignment. agent-repo-guidance then curates the repository-specific delta.

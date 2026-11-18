---
name: harness-config
description: "Use when a skill names harness-config, or when changing Pi's own profile files,
  settings, extensions, prompts, skills or packages, choosing where a Pi skill is deployed, or
  bootstrapping a repository AGENTS.md. Pi binding for edit-config, create-skill and repo guidance."
metadata:
  type: guideline
---

# Ownership

- Establish the active profile from runtime context, not the working directory or a copied profile
  name. Profile files live under `~/.config/pi/profiles/<profile>/` and are chezmoi targets; their
  source is `dot_config/pi/profiles/<profile>/` in the chezmoi repository. Persistent changes go
  through that source and edit-config's lifecycle.
- Skills installed from QStack are symlinks into a QStack clone. Resolve an installed skill's
  symlink to find it, and edit the skill in that repository, not through the link's parent
  directory and not in chezmoi.
- Pi's Git/npm package manager owns fetched plugins, extensions and skill caches. Change an owned
  fork and its installation declaration, then update only that package through the manager.
- Auth, model registries, session stores and other runtime state stay out of tracked source.
- Session history for a rehearsal comes from the active profile's session store or T3 thread
  search, with the human sender established from message provenance.

# Settings semantics

- Pi has no native settings-editing skill. Read the installed Pi docs and the profile's actual
  `settings.json`, `permissions.json` and `mcp.json` schemas before changing them.

# Skill loading

- Skills load as `<name>/SKILL.md` from the active profile's `skills/` directory and from installed
  packages. Default directory discovery stops descending once a directory has a `SKILL.md`: a
  nested child is not independently advertised merely because it has valid frontmatter. Keep
  children on explicit parent routes and verify explicit-path loading before relying on separate
  invocation.
- Claude invocation controls (`disable-model-invocation`, `context: fork` and similar) are not Pi
  configuration; do not copy them into a Pi skill.
- Changes are checked in a fresh Pi session on the intended profile.

# Guidance bootstrap

- Pi has no guidance bootstrap. Draft `AGENTS.md` from the inspected repository per
  agent-repo-guidance and name that boundary.

# QStack

Personal agent skills, installed into Claude Code and Pi as symlinks. Read `README.md` for the
layout. Author skills with the `create-skill` skill.

## Rules

- Edit skills here, never through an installed link's parent directory, chezmoi, or a plugin cache.
- `shared/` stays harness-neutral: no native tool names, slash commands or profile paths. When a
  shared skill needs harness behavior, name a `harness-*` skill and put one skill of that name in
  both `claude/` and `pi/`. Prefer extending an existing `harness-*` skill to adding a new name;
  every advertised skill costs context in every session.
- Shared skills reference each other with sibling-relative paths (`../git/SKILL.md`). They
  reference harness skills by name only, because the relative path differs per harness.
- `pi/` targets Pi running inside T3 Code. T3 MCP tools (`delegate_task` and the like) are shared
  ground and may appear in `shared/`.
- Model names, efforts and provider routing belong in `shared/subagents/model-selection` and the
  council's Panels section, not scattered through other skills.
- A skill teaches one capability: a recipe for doing a thing. Where and to what it is applied
  comes from the context, not the skill. Keep the staged procedure `create-skill` defines, which
  weaker models need, but make each step demand only what the capability itself needs. Do not
  invent requirements for the sake of rigor, and do not assume the situation: a skill about
  writing good PRs must work on a PR you did not open or in a repository that is not yours, and
  must not stretch to cover issues.
- Line count is not the measure; a skill is as long as its content needs. Prefer a sentence the
  user can edit to a config file or a helper script; skills carry no `bin/` directories.
- `claude/APPEND_SYSTEM.md` and `pi/APPEND_SYSTEM.md` are added to every session's system prompt
  by `bin/qstack install`. Put a line there only when a skill cannot work without a standing
  reminder; every line costs context in every session.
- Commit messages are conventional commits. No model or agent tool is credited as a co-author.
- Prose in this repository follows the `deslop` skill.

## Checks

Run both before committing:

```sh
bin/qstack check
python3 -m unittest discover -s tests
```

`bin/qstack check` validates frontmatter, that `claude/` and `pi/` offer the same names, and that
every relative link resolves in each harness's installed view. It does not prove a model selects
or follows a skill; that takes a rehearsal in a fresh session.

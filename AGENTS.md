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
- Model names belong in `shared/council/roster.yaml` and `shared/subagents/model-selection`, not
  scattered through other skills.
- Scripts delete with `trash-put`, never `rm`.

## Checks

Run both before committing:

```sh
bin/qstack check
python3 -m unittest discover -s tests
```

`bin/qstack check` validates frontmatter, that `claude/` and `pi/` offer the same names, and that
every relative link resolves in each harness's installed view. It does not prove a model selects
or follows a skill; that takes a rehearsal in a fresh session.

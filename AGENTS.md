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
- Write skills as loose, plain-English descriptions of what is wanted, in the Contract/Entrypoint
  shape `create-skill` defines. Do not pile on guards, templates and edge-case procedure. Line
  count is not the measure: a skill is as long as its content needs. Prefer a sentence the user
  can edit to a config file or a helper script; skills carry no `bin/` directories.
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

# QStack

The agent skills I use every day in T3 Code, kept apart from my system configuration.
Inspired by [tstack](https://github.com/t3dotgg/tstack) and
[pstack](https://github.com/cursor/plugins/tree/main/pstack).

## Layout

```
shared/   skills that read the same in every harness
claude/   Claude Code bindings
pi/       Pi bindings (the T3 profile)
bin/      qstack: check the repo, link skills into a harness
tests/    python3 -m unittest discover -s tests
```

A shared skill never describes harness mechanics. Where behavior differs it names a
`harness-*` skill, and `claude/` and `pi/` each supply a skill under that same name. A harness
installs `shared/` plus its own folder, so the name resolves to the right binding.

| Named skill | Claude Code | Pi |
| --- | --- | --- |
| `harness-delegation` | native Agent or T3 `delegate_task`, `/code-review` | always T3 `delegate_task` |
| `harness-config` | settings, skill roots, `/update-config`, `/init` | profiles, loader rules, packages |
| `harness-verification` | native `/verify` | direct reproduce, trace, repair, verify |

## Skills

| Skill | Say | What it does |
| --- | --- | --- |
| `full-send` | "full send" | Takes a change to a merged PR with nobody watching. |
| `full-stop` | "full stop" | Same, but stops with the PR ready for me to merge. |
| `council` | "council" | Review from a roster of models: paired models merged into one seat and compared, jesters as non-blocking advisors, bounded rounds, and a re-architecture when the council will not converge. |
| `subagents` | (automatic) | Delegation shape, briefs, acceptance; `model-selection` picks child models. |
| `estimate-time` | (automatic) | Measured durations for agent work. |
| `runtime-verification` | (automatic) | Evidence tiers for proving a change. |
| `git` | (automatic) | Repositories, branches, PRs, issues, project init, mirroring. |
| `create-skill` | (automatic) | Authoring and rehearsing skills. |
| `edit-config` | (automatic) | Persistent configuration through its owning source. |
| `agent-repo-guidance` | (automatic) | AGENTS.md / CLAUDE.md for a repository. |
| `project-plan` | (automatic) | Plans and architecture documents. |

### Council

Edit `shared/council/roster.yaml` to change who sits. A seat with several models (GPT 6.2 Sol
and 6.1 Sol today) is one voice: both review, their findings merge, and every round logs which
did better and what each missed. `shared/council/bin/council-log summary` totals that across runs.

## Install

```sh
bin/qstack check                              # validate names, pairs and links
bin/qstack install claude --dry-run           # ~/.claude/skills
bin/qstack install pi --profile t3main        # ~/.config/pi/profiles/t3main/skills
bin/qstack install claude --only council,harness-delegation
bin/qstack status claude
```

Each skill becomes one symlink. `install` refuses to replace anything that is not already a
QStack link, so a copy still owned by chezmoi shows up as a conflict instead of being overwritten.

## Credits

`full-send`, `full-stop` and the starting point for `council` come from tstack (MIT, Theo Browne).

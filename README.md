# QStack

These are the agent skills I use every day. I run them with Claude Code and Pi
inside [T3 Code](https://github.com/pingdotgg/t3code).

I like Theo's [tstack](https://github.com/t3dotgg/tstack) and Poteto's
[pstack](https://github.com/cursor/plugins/tree/main/pstack), and I wanted a set of skills like
theirs that I could afford to run. tstack is written for someone with a top-tier plan at every
frontier lab, who can put several frontier models on each decision. I give each model the jobs it
does well instead, and I use open-weight models like DeepSeek and GLM wherever they hold up,
because OpenCode Go makes them cheap enough to run all day.

## How the models are split up

- **Delegated work** such as scoped changes, bug diagnosis and research goes to GLM 5.3 Flash or
  DeepSeek V4.1 Flash. When a builder fails review twice on the same requirement, the task moves
  to a frontier model.
- **Hard engineering and final review** go to GPT 6.1 Sol.
- **Several models at once** only when I say `council`. The review panel is Sol (6.2 and 6.1
  sharing one vote), Claude Opus 5.5 and Muse Ember, plus GLM 5.3 as a non-voting "jester" whose
  findings are leads to check, not votes. Design questions go to Claude Fable 5.2 and GPT 6.2
  Astra. Those two stay off code review because they cost too much for it.
- Claude models run through Claude Code. Every other model runs through Pi.

The roster is written as plain sentences in
[`shared/subagents/model-selection/SKILL.md`](shared/subagents/model-selection/SKILL.md) and the
Panels section of [`shared/council/SKILL.md`](shared/council/SKILL.md). To use your own models,
edit those two files.

## Skills

Four skills start on a phrase you type:

| Say | What happens |
| --- | --- |
| `council` | A panel of models reviews a change until every voting seat scores 9/10 (or the number you give, as in `council 9.5`), or advises on a design. |
| `full stop` | The agent finishes the task on its own and stops at a ready-to-merge PR. |
| `full send` | Same as `full stop`, then it merges the PR once it passes full-stop's readiness gate. |
| `reflect` | The agent pulls lessons from the conversation and proposes edits to existing skills. Adapted from pstack. |

The rest load when the task matches their description:

| Skill | Use |
| --- | --- |
| `subagents` | Delegating work to child agents, with `model-selection` inside it for picking models |
| `runtime-verification` | Deciding how much evidence a fix or change needs before calling it done |
| `estimate-time` | Estimating how long agent work takes, from measured per-model times |
| `git` | Cloning, branching, committing, issues and PRs, with `pr`, `issues`, `init-project` and `github-mirror` inside it |
| `project-plan` | Project plans, architecture docs and roadmaps |
| `agent-repo-guidance` | Writing or fixing a repository's AGENTS.md or CLAUDE.md |
| `create-skill` | Writing and testing new skills |
| `edit-config` | Changing dotfiles and app settings through their owner, such as chezmoi |
| `deslop` | Writing prose people will read, this README included |

`claude/` and `pi/` each hold three `harness-*` skills with the same names: `harness-config`,
`harness-delegation` and `harness-verification`. The shared skills refer to them by name, so the
same `subagents` skill launches children through whichever harness loaded it.

Some skills assume my setup. `git` expects a Forgejo origin with GitHub mirrors, `edit-config`
expects chezmoi, and `council` and `subagents` need T3 Code's `delegate_task` tool. Read a skill
before you install it.

## Install

You need Python 3.

```sh
git clone https://github.com/Quinntyx/QStack
cd QStack
bin/qstack install claude                  # links into ~/.claude/skills
bin/qstack install pi --profile <name>     # links into ~/.config/pi/profiles/<name>/skills
```

Each skill is installed as a symlink into the clone, so `git pull` updates them. Use `--dir` for
another destination, `--only council,deslop` to pick skills, and `--dry-run` to see what would
change. `install` never overwrites anything that is not already a QStack link: it reports a
conflict and leaves the file alone.

`bin/qstack status claude` shows what is linked. `bin/qstack uninstall claude` removes the links
with `trash-put`, so it needs [trash-cli](https://github.com/andreafrancia/trash-cli).

## Contributing

Repository rules are in [`AGENTS.md`](AGENTS.md). Run both checks before committing:

```sh
bin/qstack check
python3 -m unittest discover -s tests
```

`bin/qstack check` validates frontmatter, checks that `claude/` and `pi/` offer the same skill
names, and resolves every relative link as each harness will see it once installed. It cannot
tell you whether a model picks up and follows a skill. That takes a run in a fresh session.

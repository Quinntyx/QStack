# QStack

QStack is the set of skills I give my coding agents. I run them in
[T3 Code](https://github.com/pingdotgg/t3code), with Claude Code and Pi as the agents. I started it
after reading Poteto's [PStack](https://github.com/cursor/plugins/tree/main/pstack) and Theo's
[TStack](https://github.com/t3dotgg/tstack), and the `reflect` skill is adapted from PStack.

A skill is a folder with a `SKILL.md` file: a description that tells the agent when to load it,
then the instructions it follows.

These skills are written for my setup. Some name my Forgejo server, my GitHub account and the
models I pay for, and `council` and `subagents` launch agents through T3 Code's MCP tools
(`delegate_task`, `orchestrator_capabilities`). Read a skill before you install it and expect to
edit it.

## Layout

- `shared/` has the skills both agents get.
- `claude/` and `pi/` each have `harness-config`, `harness-delegation` and
  `harness-verification`, written for that agent. Shared skills name these and never a
  Claude Code or Pi tool directly. For example, `subagents` decides how to split the work, and
  `harness-delegation` says how Claude Code or Pi launches each child.
- `bin/qstack` checks the repository and installs skills as symlinks.

## Skills I trigger by phrase

- **full stop**: the agent finishes the task, tests it, reviews it, opens a pull request and
  watches it until it is ready to merge, then hands it back to me without merging.
- **full send**: everything `full stop` does, then the agent merges the pull request once its
  checks and review pass.
- **council**: the agent sends a change or a design question to a panel of other models. For a
  change, it fixes what they find and sends it back until every voting model scores it at least
  9/10, or the number I give ("council 9.5"). After three rounds without agreement it asks a
  design panel for a different approach. The panels are plain lists near the bottom of
  `shared/council/SKILL.md`.
- **reflect**: the agent goes back through the conversation for lessons worth keeping and
  proposes each one as an edit to an existing skill.

## Other skills

| Skill | What it does |
| --- | --- |
| `agent-repo-guidance` | Writes or repairs a repository's `AGENTS.md` or `CLAUDE.md` |
| `create-skill` | Writes, revises and checks skills in the Contract/Entrypoint shape every skill here uses |
| `deslop` | Rules for prose a person will read. This README follows it |
| `edit-config` | Changes persistent configuration through the tool that owns it, such as chezmoi or a package manager, instead of editing the live file |
| `estimate-time` | Estimates how long agent work will take from measured per-model times |
| `git` | Cloning, branches, worktrees, commits and pushes, with child skills for `init-project`, `github-mirror`, `issues` and `pr` |
| `project-plan` | Project plans, architecture documents and `PLAN.md` |
| `runtime-verification` | Decides what evidence a bug fix or change needs, from a failing test to a real user flow |
| `subagents` | Splits work across child agents and checks what they return. Its `model-selection` child picks the models |

## Install

You need Python 3, plus `trash-put` from trash-cli if you want to uninstall.

```sh
git clone https://github.com/Quinntyx/QStack.git
cd QStack
bin/qstack install claude              # links into ~/.claude/skills
bin/qstack install pi --profile NAME   # links into ~/.config/pi/profiles/NAME/skills
```

Each skill is one symlink into the clone, so a `git pull` updates the installed skills. Other
options:

- `--dir DIR` installs somewhere else.
- `--only council,deslop` installs just those skills.
- `--dry-run` prints what would change.

`install` never replaces a folder that is not already a QStack link. It reports a conflict and
leaves the folder alone. `bin/qstack status claude` shows the state of each link, and
`bin/qstack uninstall claude` moves the links to the trash.

## Checks

Run both before committing:

```sh
bin/qstack check
python3 -m unittest discover -s tests
```

`bin/qstack check` validates each skill's frontmatter, that `claude/` and `pi/` offer the same
skill names, and that every relative link between skills resolves once installed. It cannot tell
whether an agent picks a skill at the right moment or follows it. For that I try the skill in a
fresh session.

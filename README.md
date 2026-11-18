# QStack

QStack is my set of agent skills. I run them in [T3 Code](https://github.com/pingdotgg/t3code)
with two harnesses, Claude Code and Pi.

I started it after reading [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Poteto
and [tstack](https://github.com/t3dotgg/tstack) by Theo. I like tstack's philosophy a lot, and I
wanted skills like it that work for someone who doesn't hold a top-tier subscription at every
frontier lab. tstack leans on running many frontier models side by side. QStack gives each model
the job it's best at and fills the cheaper seats with open-weight models. GPT Sol reviews code,
Claude Opus sits on the review panel next to it, and GLM and DeepSeek do focused work through
OpenCode Go, which is cheap enough to use all day.

## The skills

Skills in `shared/` work in both harnesses. A few jobs need harness-specific steps, so each of
those has a `harness-*` skill with the same name in `claude/` and in `pi/`.

| Skill | What it does |
| --- | --- |
| `council` | Say "council" to get a change reviewed, or a design question answered, by a panel of other models. "council 9.5" sets the score every voting seat must reach. |
| `full-stop` | Say "full stop" to have the agent finish the task on its own through a ready-to-merge PR, then hand off. |
| `full-send` | Same as `full-stop`, then merges the PR once its checks pass. |
| `reflect` | Say "reflect" to turn lessons from the current conversation into proposed edits to existing skills. Adapted from pstack. |
| `subagents` | Delegating work: parallel research, parallel implementation, integrating results, delegated review. |
| `subagents/model-selection` | Picks a model, effort and provider for each child, using the roster below. |
| `estimate-time` | Estimates how long agent work will take, from measured per-model run times. |
| `runtime-verification` | Decides what evidence a bug fix or change needs before it counts as verified. |
| `git` | Cloning, branches, worktrees, commits and pushes. Sub-skills cover `pr`, `issues`, `init-project` and `github-mirror` (Forgejo to GitHub mirroring). |
| `project-plan` | Project plans, architecture docs, `PLAN.md`. |
| `agent-repo-guidance` | Writing or repairing a repository's `AGENTS.md` / `CLAUDE.md`. |
| `create-skill` | Writing, revising and testing skills, including the Contract/Entrypoint shape these skills use. |
| `edit-config` | Changing dotfiles and app or harness configuration at its real source. |
| `deslop` | Writing prose people will read: READMEs, PR descriptions, commit messages, reports. |
| `harness-config`, `harness-delegation`, `harness-verification` | The Claude Code and Pi versions of configuration, child-agent launching and runtime checks. |

## Models

Model choices live in two places, written as plain sentences you can edit:

- [`shared/subagents/model-selection/SKILL.md`](shared/subagents/model-selection/SKILL.md) holds
  the roster. Focused work (small, independently checkable changes and evidence gathering) goes to
  GLM 5.3 Flash and DeepSeek V4.1 Flash. Frontier work goes to GPT 6.1 Sol. The file also sets
  effort per model; DeepSeek always runs at max.
- [`shared/council/SKILL.md`](shared/council/SKILL.md) holds the panels. The review panel is
  Sol (GPT 6.2 and 6.1 as one vote), Claude Opus 5.5 and Muse Ember, with GLM 5.3 as a
  non-voting "jester" whose findings are leads to check, not votes. The design panel is Claude
  Fable 5.2 and GPT 6.2 Astra, which cost too much to sit on every review.

With T3's `delegate_task`, Claude models run on the Claude Code provider and every other model runs
on Pi. A model your T3 setup doesn't list is reported as unavailable, not quietly swapped for
another, so change these files to match the models you have.

Some skills assume my setup: T3 Code's MCP tools for delegation, Forgejo with a GitHub mirror in
`git`, and [trash-cli](https://github.com/andreafrancia/trash-cli) instead of `rm`. Read a skill
before you install it.

## Install

You need Python 3. Clone the repository and link the skills into a harness:

```sh
git clone https://github.com/Quinntyx/QStack
cd QStack
bin/qstack install claude                  # links into ~/.claude/skills
bin/qstack install pi --profile NAME       # links into ~/.config/pi/profiles/NAME/skills
bin/qstack install pi --dir PATH           # or any skills directory
```

Each skill becomes one symlink, so a `git pull` updates every installed skill. `--only council,git`
installs a subset and `--dry-run` shows what would change. `install` never replaces a file or
directory that isn't already a QStack link; it reports a conflict and leaves it alone.

`bin/qstack status <harness>` lists each skill as linked, missing, stale or conflicting.
`bin/qstack uninstall <harness>` removes the links with `trash-put`.

## Contributing

Repository rules for agents and people are in [`AGENTS.md`](AGENTS.md). Run both checks before
committing:

```sh
bin/qstack check
python3 -m unittest discover -s tests
```

`bin/qstack check` validates each skill's frontmatter, that `claude/` and `pi/` offer the same
skill names, and that every relative link resolves once the skills are installed. Whether a model
picks a skill and follows it still needs a run in a fresh session.

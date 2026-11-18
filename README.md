# QStack

My agent skills, for Claude Code and Pi running inside [T3 Code](https://github.com/pingdotgg/t3code).

I built this after reading Poteto's [pstack](https://github.com/cursor/plugins/tree/main/pstack)
and Theo's [tstack](https://github.com/t3dotgg/tstack). I like tstack's philosophy a lot, but its
skills are written for someone who pays for every frontier lab's top plan and runs all of them in
council on every task. I wanted skills that work on a budget. So instead of sending everything to
every model, QStack gives each model the job it is good at, and it hands the bulk work to
open-weight models through [OpenCode Go](https://opencode.ai), which costs little enough that I
can use them freely.

## Models

The skills assume **Claude Opus 5.5 is the model you talk to**. It does the research, design,
debugging and every decision, and the skills never say so because they are written from its point
of view. If your main model is something else, expect to adjust them.

The other models each have one job:

| Job | Model |
| --- | --- |
| Builder: implements one chunk of work from an explicit brief | DeepSeek V4.1 Flash, max effort, via OpenCode Go |
| Review panel | GPT 6.1 / 6.2 Sol, Claude Opus 5.5, and GLM 5.3 as a non-voting extra opinion |
| Design panel | Claude Fable 5.2, GPT 6.2 Astra |

Fable and Astra sit only on design questions; they cost too much to run on every review. The
assignments live in two places, written in plain words so you can change them:
[`shared/subagents/model-selection/SKILL.md`](shared/subagents/model-selection/SKILL.md) and the
Panels section of [`shared/council/SKILL.md`](shared/council/SKILL.md).

## Skills

Everything in `shared/` works in both harnesses.

| Skill | Use |
| --- | --- |
| `full-stop` | Take a task from request to a PR that is ready to merge, then hand it back unmerged. Say "full stop council 9.5" to add a review council with a target score. |
| `full-send` | Everything `full-stop` does, then merge. |
| `council` | Put one question to a panel of models working blind: a design round or a scored review round. |
| `subagents` | Delegate work to child agents, including research, parallel implementation and review. `model-selection` sits inside it. |
| `git` | Clone, branch, commit, push, mirror. Contains `pr`, `issues`, `init-project` and `github-mirror`. |
| `runtime-verification` | Decide what evidence a bug fix or change needs before calling it done. |
| `project-plan` | Plan work in a `PLAN.md` that shrinks as its parts merge and is deleted when empty. I use it mostly for greenfield projects. |
| `agent-repo-guidance` | Write or repair a repository's AGENTS.md or CLAUDE.md. |
| `edit-config` | Change dotfiles and application settings at their real source. |
| `create-skill` | Write, revise and test a skill. |
| `deslop` | Write prose a person will read without it sounding machine-made. |
| `estimate-time` | Estimate how long agent work will take, from measured per-model times. |
| `reflect` | Turn lessons from the current conversation into proposed skill edits. Adapted from pstack. |

`claude/` and `pi/` each hold three `harness-*` skills (`harness-config`, `harness-delegation`,
`harness-verification`) that explain how the current harness does what the shared skills ask for:
where its settings live, how it launches child agents, how it checks a running change. Shared
skills name these by name and never mention a harness-specific tool.

Delegation goes through T3 Code's `delegate_task` MCP tool, so several skills expect T3 Code. In
T3, Claude models run on the Claude Code provider and everything else runs on Pi.

## Install

`bin/qstack` links each skill into a harness's skills directory as a symlink, so edits in this
repository take effect right away. It needs Python 3.

```sh
git clone https://github.com/Quinntyx/QStack.git
cd QStack

bin/qstack install claude                 # links into ~/.claude/skills
bin/qstack install pi --profile NAME      # links into ~/.config/pi/profiles/NAME/skills
bin/qstack install pi --dir PATH          # or any directory
```

A harness gets every skill in `shared/` plus its own folder. `--only full-stop,council` installs a
subset and `--dry-run` shows what would change. `install` never overwrites a file or directory
that is not already a QStack link; it reports a conflict and leaves it alone.

`bin/qstack status claude` shows the state of each link. `bin/qstack uninstall claude` removes the
links with `trash-put`, so it needs [trash-cli](https://github.com/andreafrancia/trash-cli).

## Changing the skills

Read [`AGENTS.md`](AGENTS.md) first. Run both checks before committing:

```sh
bin/qstack check
python3 -m unittest discover -s tests
```

`bin/qstack check` validates frontmatter, confirms `claude/` and `pi/` offer the same skill names,
and resolves every relative link as each harness will see it once installed. It cannot tell you
whether a model picks up and follows a skill; for that, try it in a fresh session.

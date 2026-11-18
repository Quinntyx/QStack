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
| `full-stop` | Take a task from request to a PR that is ready to merge, then hand it back unmerged. Say "full stop council 9.5" to add a review council with a target score. Also covers model training and long benchmarks: the expensive run is never handed to the cheap builder, and a scheduled check looks in on it every 5, 15 or 60 minutes. |
| `full-send` | Everything `full-stop` does, then merge. |
| `council` | Put one question to a panel of models working blind: a design round or a scored review round. |
| `subagents` | Delegate work to child agents, including research, parallel implementation and review. `model-selection` sits inside it. |
| `git` | Clone, branch, commit, push. Contains `pr`, `issues`, `init-project` and `github-mirror`. See the note on my setup below. |
| `runtime-verification` | Decide what evidence a bug fix or change needs before calling it done. |
| `project-plan` | Plan work in a `PLAN.md` that shrinks as its parts merge and is deleted when empty. I use it mostly for greenfield projects. |
| `agent-repo-guidance` | Write or repair a repository's AGENTS.md or CLAUDE.md. |
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

Some of `git` describes my own setup. I keep repositories on a Forgejo server that mirrors them
to GitHub, so `github-mirror` is only useful if you do the same, and `init-project` bootstraps a
repository that way. The hosts, account names and paths are all in one "My setup" section at the
bottom of [`shared/git/SKILL.md`](shared/git/SKILL.md). Replace it with yours before you use
`git`.

## Install

`bin/qstack` links each skill into a harness as a symlink, so edits in this repository take
effect right away. It needs Python 3.

```sh
git clone https://github.com/Quinntyx/QStack.git
cd QStack

bin/qstack install claude                    # ~/.claude, or $CLAUDE_CONFIG_DIR if set
bin/qstack install claude --home ~/.claude-work   # another Claude Code config directory
bin/qstack install pi --profile NAME         # ~/.config/pi/profiles/NAME
bin/qstack install pi --dir PATH             # any skills directory, for either harness
```

A harness gets every skill in `shared/` plus its own folder. `--only full-stop,council` installs a
subset and `--dry-run` shows what would change. `install` never overwrites a file or directory
that is not already a QStack link; it reports a conflict and leaves it alone.

`status` and `uninstall` take the same target options for both harnesses:

```sh
bin/qstack status claude --home ~/.claude-work
bin/qstack status pi --profile NAME
bin/qstack uninstall pi --profile NAME
```

`status` prints one line per skill: `linked`, `missing`, `stale` (a QStack link to the wrong
place), `conflict` or `foreign-link` (something of yours is in the way). `uninstall` removes the
links with `trash-put`, so it needs [trash-cli](https://github.com/andreafrancia/trash-cli).

### The system prompt add

`estimate-time` only works reliably when the agent is reminded, in every session, that agent work
takes minutes and hours and that the skill exists. A skill description alone does not do that,
because nothing triggers it when a model is about to write "this will take two weeks". So each
harness folder has an `APPEND_SYSTEM.md` with that reminder, and `install` adds it:

- **Claude Code:** as the link `rules/qstack.md` in the config directory. Claude Code loads every
  file in `rules/` at the start of a session.
- **Pi:** as a block between `<!-- qstack:begin -->` and `<!-- qstack:end -->` in the profile's
  `APPEND_SYSTEM.md`. The rest of the file is left as it is, and a later `install` updates the
  block in place.

Pass `--no-system` to skip it. `--dir` skips it too, since a bare skills directory has no place
for one. If a dotfile manager owns your Pi profile, the block will show up there as a change to
commit.

## Changing the skills

Read [`AGENTS.md`](AGENTS.md) first. Run both checks before committing:

```sh
bin/qstack check
python3 -m unittest discover -s tests
```

`bin/qstack check` validates frontmatter, confirms `claude/` and `pi/` offer the same skill names,
and resolves every relative link as each harness will see it once installed. It cannot tell you
whether a model picks up and follows a skill; for that, try it in a fresh session.

# QStack

My agent skills, for Claude Code and Pi running inside [T3 Code](https://github.com/pingdotgg/t3code).

I started from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Poteto and
[tstack](https://github.com/t3dotgg/tstack) by Theo. tstack assumes you pay for a subscription at
every frontier lab and can put all of them on every review and let them hill-climb. I can't, so
QStack gives each model the job it is good at and hands the rest to open-weight models. GPT Sol
reviews code, with Claude Opus beside it. GLM, DeepSeek and MiMo do the bounded work, and through
OpenCode Go they cost little enough to use all the time.

## What's in it

Most skills are harness-neutral and live in `shared/`. Each harness also gets three small
`harness-*` skills that say how that harness does the thing a shared skill asks for.

| Skill | Use it for |
| --- | --- |
| `council` | Say "council" to get a change reviewed, or a design question answered, by a panel of models. "council 9.5" sets the score every voting seat must reach. |
| `full-stop` | Say "full stop" to have the agent finish the task through a ready-to-merge PR and hand off. |
| `full-send` | Say "full send" for everything `full-stop` does, plus merging when the PR's gate passes. |
| `reflect` | Say "reflect" to turn lessons from the conversation into proposed edits to existing skills. Adapted from pstack. |
| `subagents` | Delegating work, parallel children, and how to accept or integrate what they return. |
| `subagents/model-selection` | Which model, effort and provider each child gets. |
| `runtime-verification` | How much evidence a fix or change needs before it counts as verified. |
| `estimate-time` | Sizing agent work from measured per-model times. Agent work takes minutes and hours, not days. |
| `project-plan` | Project plans, architecture docs, `PLAN.md`. |
| `agent-repo-guidance` | Writing or repairing a repository's `AGENTS.md` or `CLAUDE.md`. |
| `create-skill` | Writing, revising and testing skills, including routed skill trees. |
| `edit-config` | Changing dotfiles and app or harness settings at their real source. |
| `deslop` | Prose a person will read: READMEs, PR descriptions, commit messages, reports. |
| `git` | Cloning, branches, commits and pushes. Routes to `pr`, `issues`, `init-project` and `github-mirror`. |
| `harness-config`, `harness-delegation`, `harness-verification` | One copy each in `claude/` and `pi/`. |

Some of this is shaped around my own setup. The `git` skills assume Forgejo hosting with GitHub
mirrors, and `council`, `subagents` and `model-selection` call T3 Code's MCP tools
(`delegate_task`, `orchestrator_capabilities`). Outside T3 Code those skills have no way to launch
other models.

## How the models are used

`shared/subagents/model-selection/SKILL.md` splits work into two tiers:

- **Focused**: bounded implementation with a clear acceptance test, diagnosis, evidence gathering.
  GLM 5.3 Flash, DeepSeek V4.1 Flash, MiMo V2.6 Flash.
- **Frontier**: hard engineering, architecture, subtle review, final acceptance. GPT 6.1 Sol.

A focused builder that fails two repair reviews on the same requirement is promoted to the frontier
tier. Claude models run on the Claude Code provider and every other model runs on Pi.

The council keeps two panels, written as plain sentences in `shared/council/SKILL.md` so they are
easy to edit:

- **Review**: GPT Sol (6.2 and 6.1 as one merged seat), Claude Opus 5.5, Muse Ember, and GLM 5.3
  as a jester that does not vote and is never waited for.
- **Design**: Claude Fable 5.2 and GPT 6.2 Astra. They cost too much to sit on every review, so
  they only see design questions.

The model names are in those two files only. Change them there and every other skill follows.

## Install

`bin/qstack` links each skill into a harness's skills directory as a symlink, so editing the repo
updates the installed skill. A harness gets everything in `shared/` plus its own folder.

```sh
git clone https://github.com/Quinntyx/QStack
cd QStack

bin/qstack install claude                 # into ~/.claude/skills
bin/qstack install pi --profile NAME      # into ~/.config/pi/profiles/NAME/skills
bin/qstack install pi --dir ~/somewhere   # or any directory

bin/qstack install claude --only council,deslop --dry-run
bin/qstack status claude
bin/qstack uninstall claude
```

`install` never replaces anything that isn't already a QStack link. It reports a conflict and
leaves the file alone. `uninstall` moves links to the trash with `trash-put`, so it needs
trash-cli.

## Layout

```
shared/   skills for every harness; may name harness-* skills but no native tool names
claude/   harness-* skills for Claude Code
pi/       harness-* skills for Pi inside T3 Code
bin/      qstack: install, status, uninstall, check
tests/    unit tests for bin/qstack
```

## Contributing

Read `AGENTS.md` first. It has the rules for what goes in `shared/` versus a harness folder. Run
both checks before committing:

```sh
bin/qstack check
python3 -m unittest discover -s tests
```

`bin/qstack check` validates frontmatter, that `claude/` and `pi/` offer the same skill names, and
that every relative link resolves in each harness's installed view. It can't tell you whether a
model picks up and follows a skill. For that, try it in a fresh session.

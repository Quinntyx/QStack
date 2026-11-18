# QStack

Agent skills for Claude Code and Pi, built around [T3 Code](https://github.com/pingdotgg/t3code).
Say a phrase and the agent runs a whole workflow: ship a change without check-ins, or put it in
front of a panel of other models until they agree it is good.

QStack follows Theo's [tstack](https://github.com/t3dotgg/tstack) and Poteto's
[pstack](https://github.com/cursor/plugins/tree/main/pstack). `full-send` and `full-stop` began
as tstack's, and `reflect` as pstack's.

## What you can say

| Say | What the agent does |
| --- | --- |
| "full stop" | Finishes the change, proves it works, gets it reviewed, opens a PR and watches CI until the PR is ready to merge. It never merges. |
| "full send" | Everything "full stop" does, then merges the PR. |
| "council" | Sends a change to a panel of other models and fixes what they find, round after round, until every seat scores it 9 out of 10 or higher. Before any code exists, the same word asks a second panel which architecture to build. |
| "council 9.5" | The same review with the target raised to 9.5. |
| "reflect" | Reads the conversation for corrections you made and proposes an edit to the skill each one belongs to. Nothing changes until you approve it. |

The phrases combine. "Build the importer, full send, council 9.5" builds the importer, uses the
council as its review, and merges once the council and CI have both passed.

The other skills load on their own when the work calls for them:

| Skill | Covers |
| --- | --- |
| `subagents` | Splitting work across child agents, briefing them and accepting their results. Its `model-selection` child decides which model runs where and at what effort. |
| `estimate-time` | How long agent work takes, from measured runs. |
| `runtime-verification` | How much evidence a change needs before it counts as proven. |
| `git` | Branches, pull requests, issues, new repositories and GitHub mirrors. |
| `create-skill` | Writing a skill and rehearsing it on a cheaper model. |
| `edit-config` | Changing configuration through the source that owns it. |
| `agent-repo-guidance` | Writing a repository's `AGENTS.md` or `CLAUDE.md`. |
| `project-plan` | Plans and architecture documents. |
| `deslop` | Writing English that does not read as machine output. This README was written with it. |

## How the council works

There are two panels, and what you hand the council picks between them. A diff goes to the
review panel. A question about how to build something goes to the design panel, which seats the
most expensive models and is kept away from routine review for that reason.

The two panels are briefed in opposite ways. Reviewers receive the diff, your request and the
decisions the agent made, so they explore the code themselves and do not inherit the agent's
assumptions. The design panel receives everything the agent found, so its models spend their
tokens on the decision and not on reading the repository.

A design gets three review rounds. If the panel still will not pass it, the agent stops patching,
saves the attempt on a branch, asks the design panel which architecture it would approve, and
rebuilds from the base revision. After two rebuilds it stops and shows you the disagreement.

A seat can hold two models that count as one voice, which is how you trial a new model against
the one it might replace. A seat can also be a jester: a cheaper model whose findings count only
after the agent has confirmed them, and which nobody waits for.

Each council reply ends with tagged lines such as `sol_comparison`, recording how the paired
models did against each other. Search your threads for the tag later to compare them across
runs.

As shipped, the review panel is GPT 6.2 Sol and 6.1 Sol in one seat, Claude Opus 5.5 and Muse
Ember, with GLM 5.3 as jester. The design panel is Claude Fable 5.2 and GPT 6.2 Astra. To seat
your own models, edit the Panels section at the end of
[`shared/council/SKILL.md`](shared/council/SKILL.md). It is written as sentences.

## One skill, two harnesses

```
shared/   skills that read the same in every harness
claude/   Claude Code versions of the harness skills
pi/       Pi versions of the harness skills
```

A shared skill does not describe how a harness works. Where Claude Code and Pi differ, it names
one of three skills, and `claude/` and `pi/` each hold a skill with that name. You install
`shared/` plus one harness folder, so the name resolves to the version written for your harness.

| Skill | In Claude Code | In Pi |
| --- | --- | --- |
| `harness-delegation` | Native subagents or T3 `delegate_task`; `/code-review` for reviews | T3 `delegate_task` for every child |
| `harness-config` | Settings, skill directories, `/update-config`, `/init` | Profiles, skill discovery, packages |
| `harness-verification` | The native `/verify` workflow | Reproduce, trace, repair and verify by hand |

## Install

```sh
git clone https://github.com/Quinntyx/QStack.git
cd QStack
bin/qstack install claude                  # links into ~/.claude/skills
bin/qstack install pi --profile <name>     # links into ~/.config/pi/profiles/<name>/skills
bin/qstack status claude
```

Each skill becomes one symlink, so an edit in your clone takes effect in the next session.
`install` leaves alone anything that is not already a QStack link and reports it as a conflict.

You need `python3`, and T3 Code for the skills that delegate to other models. Several skills
name one person's setup: a Forgejo server, chezmoi for dotfiles, a particular set of models.
Fork the repository and edit those to match yours. The skills are short and written to be
changed.

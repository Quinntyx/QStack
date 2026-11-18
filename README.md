# QStack

The agent skills I use in T3 Code, under both Claude Code and Pi. They live in this repository
so that changing a skill does not mean changing my dotfiles.

The idea comes from Theo's [tstack](https://github.com/t3dotgg/tstack) and Poteto's
[pstack](https://github.com/cursor/plugins/tree/main/pstack). `full-send` and `full-stop` began
as tstack's, and `reflect` as pstack's.

## What you can say

| Say | What the agent does |
| --- | --- |
| "full stop" | Finishes the change, proves it works, gets it reviewed, opens a PR and watches CI until the PR is ready to merge. It never merges. |
| "full send" | Everything "full stop" does, then merges the PR. |
| "council" | Sends a change to a panel of other models and fixes what they find, round after round, until every seat scores it 9 or higher. Before any code exists, the same word asks a second panel which architecture to build. |
| "council 9.5" | The same review with the target raised to 9.5. |
| "reflect" | Reads the conversation for corrections I made and proposes an edit to the skill each one belongs to. Nothing changes until I approve it. |

The phrases combine. "Build the importer, full send, council 9.5" builds the importer, uses the
council as its review, and merges once the council and CI have both passed.

The rest load when the work calls for them:

| Skill | Covers |
| --- | --- |
| `subagents` | How to split work across child agents, brief them and accept their results. Its `model-selection` child decides which model runs where and at what effort. |
| `estimate-time` | How long agent work takes, from measured runs. |
| `runtime-verification` | How much evidence a change needs before it counts as proven. |
| `git` | Branches, pull requests, issues, new repositories and GitHub mirrors. |
| `create-skill` | Writing a skill and rehearsing it on a cheaper model. |
| `edit-config` | Changing configuration through the source that owns it. |
| `agent-repo-guidance` | Writing a repository's `AGENTS.md` or `CLAUDE.md`. |
| `project-plan` | Plans and architecture documents. |
| `deslop` | Writing English that does not read as machine output. This README was written with it. |

## How the council works

There are two panels, and the subject picks between them. A diff goes to the review panel: GPT
6.2 Sol and GPT 6.1 Sol sharing one seat, Claude Opus 5.5, and Muse Ember. A question about how
to build something goes to the design panel, Claude Fable 5.2 and GPT 6.2 Astra, which cost too
much to spend on routine review.

The two panels are briefed in opposite ways. Reviewers receive the diff, my request and the
decisions the agent made, so they explore the code themselves and do not inherit the agent's
assumptions. The design panel receives everything the agent found, so the expensive models spend
their tokens on the decision and not on reading the repository.

A design gets three review rounds. If the panel still will not pass it, the agent stops patching,
saves the attempt on a branch, asks the design panel which architecture it would approve, and
rebuilds from the base revision. After two rebuilds it stops and shows me the disagreement.

GLM 5.3 sits on the review panel as a jester. Its findings count only after the agent has
confirmed them, and nobody waits for it.

Each council reply ends with tagged lines: `sol_comparison` records how the two Sol models did
against each other and which effort 6.2 ran at, `glm_review` records what GLM contributed, and
`glm_flub` quotes anything it said that was funny. Searching T3 Code threads for a tag collects
them.

To change who sits on a panel, edit the Panels section at the end of
[`shared/council/SKILL.md`](shared/council/SKILL.md). It is written as sentences.

## Layout

```
shared/   skills that read the same in every harness
claude/   Claude Code versions of the harness skills
pi/       Pi versions of the harness skills
bin/      qstack, which checks the repository and installs the skills
tests/    tests for qstack
```

A shared skill does not describe how a harness works. Where the harnesses differ, it names one
of three skills, and `claude/` and `pi/` each hold a skill with that name. A harness installs
`shared/` plus its own folder, so the name resolves to the version written for it.

| Skill | In Claude Code | In Pi |
| --- | --- | --- |
| `harness-delegation` | Native subagents or T3 `delegate_task`; `/code-review` for reviews | T3 `delegate_task` for every child |
| `harness-config` | Settings, skill directories, `/update-config`, `/init` | Profiles, skill discovery, packages |
| `harness-verification` | The native `/verify` workflow | Reproduce, trace, repair and verify by hand |

## Install

```sh
git clone https://git.quinntyx.dev/quinntyx/QStack.git
cd QStack
bin/qstack install claude                  # links into ~/.claude/skills
bin/qstack install pi --profile t3main     # links into ~/.config/pi/profiles/t3main/skills
bin/qstack status claude
```

Each skill becomes one symlink, so an edit here takes effect in the next session. `install`
leaves alone anything that is not already a QStack link and reports it as a conflict.

These skills assume my setup: T3 Code for delegation, Forgejo at `git.quinntyx.dev`, chezmoi
for dotfiles. Fork the repository and edit the skills to match yours.

## Checks

```sh
bin/qstack check
python3 -m unittest discover -s tests
```

`check` confirms that every skill has valid frontmatter, that `claude/` and `pi/` offer the same
names, and that every relative link resolves once installed.

# QStack

My agent skills, for Claude Code, Pi and Antigravity, including sessions inside
[T3 Code](https://github.com/pingdotgg/t3code).

I built this after reading Poteto's [pstack](https://github.com/cursor/plugins/tree/main/pstack)
and Theo's [tstack](https://github.com/t3dotgg/tstack). I like tstack's philosophy a lot, but its
skills are written for someone who pays for every frontier lab's top plan and runs all of them in
council on every task. I wanted skills that work on a budget. So instead of sending everything to
every model, QStack gives each model the job it is good at, and it hands the bulk work to
open-weight models through [OpenCode Go](https://opencode.ai), which costs little enough that I
can use them freely.

I use agents to run a lot of work in parallel with as little hand-holding as I can manage: I
hand a task off, leave, and come back to finished work with decisions explained at the
architecture level rather than a diff to read. The skills are written for that, and they
trust the model to do the right thing. The longer version of how I think about this is
[`shared/stack-philosophy/SKILL.md`](shared/stack-philosophy/SKILL.md), which the agents read
too.

## Models

The skills assume **Claude Opus 5.5 is the model you talk to**. It does the research, design,
debugging and every decision, and the skills never say so because they are written from its point
of view. If your main model is something else, expect to adjust them.

The other models each have one job:

| Job | Model |
| --- | --- |
| Builder: implements cleanly separable chunks from an explicit brief | DeepSeek V4.1 Flash (OpenCode Go on Pi) and Hy4 Flash Free (OpenCode provider, free, tighter leash, mixed in to compare), max effort |
| Review panel | GPT 6.1 / 6.2 Sol, Claude Opus 5.5 |
| Design panel | Claude Fable 5.2, GPT 6.2 Astra |

Fable and Astra sit only on design questions; they cost too much to run on every review. The
assignments live in two places, written in plain words so you can change them:
[`shared/subagents/model-selection/SKILL.md`](shared/subagents/model-selection/SKILL.md) and the
Panels section of [`shared/council/SKILL.md`](shared/council/SKILL.md).

## Skills

Everything in `shared/` works in all three harnesses.

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
| `create-skill` | Write, revise and validate a skill. |
| `web-search` | Search the web, read pages and screenshot them. Uses the harness's own web tools, then curl, then Context.dev for pages those cannot load. |
| `deslop` | Write text that leaves the conversation, from a README to a two-line email, without it sounding machine-made. |
| `estimate-time` | Estimate how long agent work will take, from measured per-model times. |
| `stack-philosophy` | Not a procedure. The philosophy behind QStack, in the same voice as this README: how I work across parallel threads at the architecture level, keeping the codebase clean vs. YAGNI, model delegation, when to stop, and how to resolve doubt. Agents read it whenever they are unsure what to do. |
| `reflect` | Turn lessons from the current conversation into proposed skill edits. Adapted from pstack. |

`claude/`, `pi/` and `antigravity/` each hold three `harness-*` skills (`harness-config`,
`harness-delegation`, `harness-verification`) that explain how the current harness does what the
shared skills ask for:
where its settings live, how it launches child agents, how it checks a running change. Shared
skills name these by name and never mention a harness-specific tool.

Delegation goes through T3 Code's `delegate_task` MCP tool, so several skills expect T3 Code. In
T3, use the provider configured for the model. Standalone Antigravity can load the skills, but
T3-managed delegation requires a T3 session.

`web-search` falls back to [Context.dev](https://context.dev), a hosted browser and search API,
when the harness's own tools and curl cannot get a page, and for screenshots of public pages.
It needs an API key, read from `$CONTEXT_DEV_API_KEY` or `~/.config/context-dev/api_key`. The
free plan gives 1,000 credits a month without a card. A page or a screenshot costs 1 credit and
ten search results cost 1, so you should not have to pay for it.

Some of `git` describes my own setup. I keep repositories on a Forgejo server that mirrors them
to GitHub, so `github-mirror` is only useful if you do the same, and `init-project` bootstraps a
repository that way. The hosts, account names and paths are all in one "My setup" section at the
bottom of [`shared/git/SKILL.md`](shared/git/SKILL.md). Replace it with yours before you use
`git`.

## Install

`bin/qstack` links each skill into Claude Code and Pi as a symlink, so edits in this repository
take effect right away. Antigravity gets copies instead; see below. It needs Python 3.

```sh
git clone https://github.com/Quinntyx/QStack.git
cd QStack

bin/qstack install                           # all three harnesses
bin/qstack install claude pi antigravity      # the same, explicitly
bin/qstack install claude antigravity         # just these two
bin/qstack install claude                    # ~/.claude, or $CLAUDE_CONFIG_DIR if set
bin/qstack install claude --home ~/.claude-work   # another Claude Code config directory
bin/qstack install pi --profile NAME         # ~/.config/pi/profiles/NAME
bin/qstack install antigravity               # ~/.gemini/config/skills; system or T3-managed
bin/qstack install antigravity --home ~/.gemini-work  # another Gemini directory
bin/qstack install antigravity --dir .agents/skills   # project skills only
```

A harness gets every skill in `shared/` plus its own folder. `--only full-stop,council` installs a
subset and `--dry-run` shows what would change. These options apply to every selected target.
`install` never overwrites a file or directory that is not already a QStack link; it reports a
conflict, continues with the other targets, and exits unsuccessfully if any target had conflicts.

Pi needs no explicit target: it uses `--profile NAME`, then `--home DIR`, then
`$PI_CODING_AGENT_DIR` if set. Otherwise it installs into every existing profile under
`~/.config/pi/profiles/`, or `~/.pi/agent` if there are no profiles. `--profile` selects only Pi's
target in a multi-harness command. `--home` and `--dir` require exactly one harness so different
harnesses cannot overwrite each other's bindings in a shared destination.

`status` and `uninstall` take the same target options for all three harnesses:

```sh
bin/qstack status claude pi antigravity
bin/qstack status claude --home ~/.claude-work
bin/qstack status pi --profile NAME
bin/qstack status antigravity
bin/qstack uninstall pi --profile NAME
bin/qstack uninstall antigravity
```

`status` and `uninstall` accept multiple harness names but require at least one explicit name, and
`uninstall` also honors `--no-system`. Each command prints the harness and skills directory before
its results.

`status` prints one line per skill: `linked` (installed and current), `missing`, `stale` (a
QStack link to the wrong place, or an outdated copy), `orphaned` (a QStack-owned entry whose skill
no longer exists for that harness), and `conflict` or `foreign-link` (something of yours is in the
way). Full `install` and `uninstall` (without `--only`) remove orphaned QStack skills with
`trash-put` while leaving non-QStack entries untouched. `uninstall` also uses `trash-put` to remove
installed links and copies, and `install` uses it to replace outdated Antigravity copies, so both
need [trash-cli](https://github.com/andreafrancia/trash-cli).

### Antigravity installations

`bin/qstack install antigravity` uses Antigravity's global skills directory,
`~/.gemini/config/skills/`. It works with a system installation and with the ACP runtime installed
by T3 Code's **Install Antigravity** button. The managed executable need not be on `PATH`: QStack
installs skills into the user directory, not the runtime's download directory.

Antigravity's file tools refuse to read a file whose real path is outside the workspace or its
skills directory, so a symlinked skill shows up in the skill list but its `SKILL.md` cannot be
opened. QStack therefore copies each skill directory, with a `.qstack-source` file naming where it
came from. Run `bin/qstack install antigravity` again after editing a skill; `status` marks
outdated copies `stale`, and `install` replaces them, overwriting any edits made to the copies.
`install` also converts the symlinks older QStack versions made.

T3 gives each Antigravity provider session a private `GEMINI_HOME` and links global skills from
the real `~/.gemini` into it. QStack therefore uses `~/.gemini` even if `GEMINI_HOME` is set. Start
a new T3 provider session after installing so T3 can prepare those links. `--home` is an explicit
override for a standalone custom home; T3's normal profile setup still uses the real `~/.gemini`.

QStack does not install Antigravity, select T3's binary, sign in, or edit T3's private profiles.
See [Google's discovery paths](https://antigravity.google/docs/customization-discovery/) and
[T3's provider guide](https://github.com/pingdotgg/t3code/blob/main/docs/user/providers-antigravity.md).

### The system prompt add

Two skills only work reliably when the agent is reminded of them in every session.
`estimate-time` needs the agent to know that agent work takes minutes and hours and that the
skill exists. A skill description alone does not do that, because nothing triggers it when a
model is about to write "this will take two weeks". `deslop` needs to be loaded before any text
that leaves the conversation, and without a reminder agents skip it for short text: asked to
commit a staged change, they wrote the message without it because the message was short. So
each harness folder has an `APPEND_SYSTEM.md` with both reminders, and `install` adds it:

- **Claude Code:** as the link `rules/qstack.md` in the config directory. Claude Code loads every
  file in `rules/` at the start of a session.
- **Pi:** as a block between `<!-- qstack:begin -->` and `<!-- qstack:end -->` in the profile's
  `APPEND_SYSTEM.md`. The rest of the file is left as it is, and a later `install` updates the
  block in place.
- **Antigravity:** as the same marked block in `~/.gemini/GEMINI.md`, or `GEMINI.md` under
  `--home`. Antigravity reads `~/.gemini/GEMINI.md` even when `GEMINI_HOME` points elsewhere,
  so T3's managed sessions get it too. Antigravity's block also tells the agent not to name
  files in replies unless asked, to re-read its active skills and their references after its
  context is compacted (because Antigravity's compaction summary does not keep them), and to
  narrow searches and pass line ranges on large code files so context stays below 200k tokens.

Pass `--no-system` to skip it. `--dir` skips it too, since a bare skills directory has no place
for one. `--only` also skips the prompt. If a dotfile manager owns the target prompt file, the
block will show up there as a change to commit.

## Changing the skills

Read [`AGENTS.md`](AGENTS.md) first. Run both checks before committing:

```sh
bin/qstack check
python3 -m unittest discover -s tests
```

`bin/qstack check` validates frontmatter, confirms all harness folders offer the same skill names,
and resolves every relative link as each harness will see it once installed. It cannot tell you
whether a model picks up and follows a skill; validate that in real work and revise the skill when
issues show up.

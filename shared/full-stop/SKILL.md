---
name: full-stop
description: "Use when the user says 'full stop', even as closing emphasis — carry the task on
  your own from request to a PR that is ready to merge, then hand it back unmerged. Also reads
  the council phrases that can follow it ('full stop council 9.5', '10x council', 'unlimited
  council', 'council 9.5 comp <thing>')."
metadata:
  type: procedure
---

# Contract

## Input Contract

- A request containing "full stop", plus the current work state (branch, diff, PR). The task
  need not be plain implementation: training a model or running a long benchmark goes through
  the same stages.
- Push rights on the repository and visibility of its CI and reviews.
- `full-send` runs stages 1–9 with its own grant, then merges instead of handing off.

## Output Contract

- The PR open, unmerged and ready per the Readiness gate, or a blocked state with one question.
- A handoff naming the PR link, final head, verdict, proof, remaining risks and the decisions you
  made for the user. If a council ran, each round's scores, and the council skill's tagged notes copied in
  word for word, one per line, so a later search of the conversation finds them.
- No PR watch or check-back schedule left active, and no delegate left running.

# Entrypoint

## Stage 1: Grant and request

The user is not watching this thread. Own the work and decide what you can yourself.

"Full stop" grants, for this task only: committing, pushing, rebasing and `--force-with-lease` on
the task's own branches, and any test method proof needs without asking first — computer use,
browser automation, simulators, running the app or a dev server, screenshots. That replaces an
ask-first rule in a project file; rules naming the right command or fixture still apply.

It does not grant merging, deleting data, touching production, changing anything outside the
repository, closing the PR, force-pushing another branch or bypassing an approval prompt. Never
merge, enable auto-merge, enter a merge queue or push to the default branch. Turn off existing
auto-merge before you start, check again before each push, and report it.

Read the words after "full stop". They are settings for Stage 7, not a request to load another
skill:

| Phrase | Meaning |
| --- | --- |
| `council` | Hold a review council before the PR opens. The target score is 9. |
| `council 9.5` | The same, with 9.5 as the target. |
| `10x council 9.5` | Allow up to 10 review rounds. Without a count the cap is 5. |
| `unlimited council 9.5` | No cap. Keep going until rounds stop producing progress. |
| `council 9.5 comp X and Y` | Also score X and Y, and require ours to beat each. `compare` and `comparison` mean the same. |

"Improve our UI full stop unlimited council 9.5 comp ChatGPT Codex and Claude Code Desktop"
means: improve the UI, review it until every voting seat scores it at least 9.5 and above both of
those products, with no round cap. Without the word "council", no review council runs.

## Stage 2: Design

On the default branch, pick the task branch with `../git/SKILL.md` first.

If the repository has a `PLAN.md`, the request is usually one of its parts. Read it: its
decisions bind this work.

Research the request yourself: read the code it touches, and search the web for how others have
built the same thing when that would inform the design.

If the request turns on a significant architecture choice, or asks you to be creative, hold a
design round with `../council/SKILL.md` and hand it everything you found. While it runs, work
out the design you would choose. When it returns, compare the proposals with yours point by
point. Lean toward the council where you differ, and hold your position where its members missed
something you can show. Choose one architecture from that mix.

A model training recipe and its hyperparameters are architecture choices of this kind: the
data, the objective, the schedule, the model size and the evaluation. So is the setup of a
long benchmark. Hold the design round before spending the compute.

Otherwise, choose the design yourself.

When the whole change is small enough that writing a builder's brief would take longer than
making it, a few dozen lines at most, make it yourself and go to Stage 5.

## Stage 3: Plan

Write `ARCHITECTURE.md` at the root of the worktree: every design decision, then the work split
into chunks, each sized for one builder to finish alone, with the files it owns and how to tell
it is done. It is a working file that dies with the worktree. Never commit it; add it to
`.git/info/exclude`, and use another name if the repository already tracks one.

If the project has a linter configured, add the lint rules that can check the design
mechanically, such as a forbidden import or a required boundary. A rule the linter enforces is
one a builder cannot drift from.

## Stage 4: Build

Give each chunk to a builder through `../subagents/SKILL.md`, on the builder model named in
`../subagents/model-selection/SKILL.md`. Write each brief so the builder has no architecture left
to decide and little to explore: the chunk from `ARCHITECTURE.md`, the decisions that constrain
it, the exact files and symbols, the patterns in the repository to copy, the commands that check
it, and what is out of scope.

Builders work in the task's own checkout, so their work lands where you can read it. Chunks
that own different files run in parallel; a chunk that needs another chunk's result waits for
it.

**Where failure is expensive, do the work yourself.** A builder is cheap because its mistakes
are cheap to catch and redo. That stops being true when a mistake burns hours of compute or
cannot be undone: launching a training run, running a long benchmark, a migration over real
data. Builders can still write what comes before that step, such as the data loader, the
harness or the config plumbing, and you read it as in Stage 5. The expensive step itself, and
the code whose mistakes would only show up during it, you write and run yourself.

A run too long to sit through in one turn follows `references/long-runs.md`.

## Stage 5: Check and converge

Read what came back until you understand what was written. Then check it against
`ARCHITECTURE.md` and the request:

- Run the app and the basic flows. Use whatever Stage 1 grants: the preview browser, a dev
  server, simulators, screenshots. `../runtime-verification/SKILL.md` picks how much evidence the
  change needs.
- Look for parts of the request that are missing and for code that departs from the design.

This is a check that the work is all there and holds together. Leave rare edge cases and deep bug
hunts alone at this stage.

When something is missing or off the design, correct the brief, add a lint rule if one would have
caught it, and send it back to a builder. Then check again. Repeat until the change does what
`ARCHITECTURE.md` says.

Commit after each check, with a conventional commit message unless the repository uses another
format. The first commit is usually `feat`, or `fix` when the whole PR is a fix. What you
found and repaired afterwards goes in as `fix`, `chore` and the like.

## Stage 6: Clean up

Make the diff small, and limited to the change that was asked for.

- Read every test that was added. Delete the ones that would not catch a real mistake.
- Delete comments that narrate the code or restate it.
- Run the project's formatter and linter.
- Remove anything the request did not ask for.
- When the work came from `PLAN.md`, delete the part you built from it, and delete the file if
  nothing is left. `PLAN.md` lists only work that has not merged.

Commit the cleanup.

## Stage 7: Council review

Without "council" in the request, go to Stage 8.

With it, read `references/council-review.md` and follow it. Come back here when the council
passes. If it does not pass, that file says what to do instead.

## Stage 8: Open the PR

Run Stage 6 again over anything the review rounds added. Rebase onto the latest tip of the
branch the PR targets and open the PR with `../git/pr/SKILL.md`. The description states the change and one line on how
you proved it.

## Stage 9: CI and comments

If the PR has CI, wait for it to pass and fix what fails. If you end your turn while checks are
pending, nothing wakes you: in T3 Code call `watch_pull_request` first.

Read the comments that arrived on the PR while you waited and answer each as you judge right,
with `../git/pr/SKILL.md`. Then read the live PR and name the verdict against the Readiness
gate: **ready**, **waiting for required human approval**, or **blocked**.

## Stage 10: Hand off

Leave the PR open and unmerged. Call `unwatch_pull_request`, then report per the Output Contract
and say plainly that the PR is still open.

# Readiness gate

All true on the latest commit: you have run the change and seen it work; a requested council
passed; required checks are green; review bots have finished and each finding is fixed or
dismissed with a reason; no human review requests changes; the branch is up to date and the host
calls it mergeable; the PR is open and not a draft.

# Asking the user

Ask only when you cannot continue alone: you cannot get the change to work, the gate cannot pass,
the next step is outside the grant, the goal is ambiguous in a way that changes the result, or
another PR makes this one obsolete. Unwatch the PR, then end your turn with the question as the
final message: the PR link if there is one, what blocks you, and the options with your
recommendation first. Decide everything else yourself and list those decisions in the report.

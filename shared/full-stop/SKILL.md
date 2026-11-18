---
name: full-stop
description: "Use when the user says 'full stop', even as closing emphasis — finish the task
  autonomously through a ready-to-merge PR, then hand off without merging."
metadata:
  type: procedure
---

# Contract

## Input Contract

- A request containing "full stop", plus the current work state (branch, diff, PR).
- Push rights on the repository and visibility of its CI and reviews.
- `full-send` reuses stages 2–6 with its own grant, then merges instead of handing off.

## Output Contract

- The PR open, unmerged and ready per the Readiness gate, or a blocked state with one question.
- A handoff naming the PR link, final head, verdict, proof, review outcome, remaining risks and
  the decisions you made for the user.
- No PR watch left active.

# Entrypoint

## Stage 1: Grant and boundary

The user is not watching this thread. Own the work and decide what you can yourself.

"Full stop" grants, for this task only: committing, pushing, rebasing and `--force-with-lease` on
the task's own branch, and any test method proof needs without asking first — computer use,
browser automation, simulators, running the app or a dev server, screenshots. That replaces an
ask-first rule in a project file; rules naming the right command or fixture still apply.

It does not grant merging, deleting data, touching production, changing anything outside the
repository, closing the PR, force-pushing another branch or bypassing an approval prompt. Never
merge, enable auto-merge, enter a merge queue or push to the default branch. Turn off existing
auto-merge before you start, check again before each push, and report it.

## Stage 2: Finish the change

Complete the goal with the smallest change that works. Fix the case that happened, not every case
that could. On the default branch, pick the task branch with `../git/SKILL.md` first. If the user
asked for a council and the task turns on an architecture choice, take that choice to the
`council` skill's design panel before building. Parallel work follows `../subagents/SKILL.md`.

## Stage 3: Prove it

Every change in the diff maps to evidence you observed yourself in this session: a reproduction
that failed and now passes, the checks CI runs, the app running with the change in it. Use
`../runtime-verification/SKILL.md` to pick how much evidence the change needs. Green mocked tests
do not prove a UI works. If you cannot prove a change, ask.

## Stage 4: Review

Get one independent review and fix its real findings, with proof for each fix. If the user said
"council", the `council` skill is the review, and a number after it ("council 9.5") is the score
it must reach. Otherwise use the review route the `harness-delegation` skill names. Review must
cover the final diff.

## Stage 5: File the PR

Rebase onto the latest default branch. The description states the change and one line on how you
proved it. `../git/pr/SKILL.md` owns the details.

## Stage 6: Babysit to readiness

Fix findings and CI failures until the Readiness gate passes. If you end your turn while checks
are pending, nothing wakes you: in T3 Code call `watch_pull_request` first. Then read the live PR
and name the verdict: **ready**, **waiting for required human approval**, or **blocked**.

## Stage 7: Hand off

Leave the PR open and unmerged. Call `unwatch_pull_request`, then report per the Output Contract
and say plainly that the PR is still open.

# Readiness gate

All true on the latest commit: your proof covers every change; required checks are green; review
bots have finished and each finding is fixed or dismissed with a reason; no human review requests
changes; the branch is up to date and the host calls it mergeable; the PR is open and not a draft.

# Asking the user

Ask only when you cannot continue alone: you cannot prove the change, the gate cannot pass, the
next step is outside the grant, the goal is ambiguous in a way that changes the result, or another
PR makes this one obsolete. Unwatch the PR, then end your turn with the question as the final
message: the PR link, what blocks you, and the options with your recommendation first. Decide
everything else yourself and list those decisions in the report.

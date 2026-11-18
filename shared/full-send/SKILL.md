---
name: full-send
description: "Use when the user says 'full send' — do everything 'full stop' does, then merge
  the PR once it is ready. Takes the same council phrases ('full send council 9.5')."
metadata:
  type: procedure
---

# Contract

## Input Contract

- A request explicitly containing "full send", plus the current work state (branch, diff, PR).
- Everything `../full-stop/SKILL.md` needs, plus merge authority on the repository.

## Output Contract

- A merged PR, or the PR left open and unmerged with one focused question.
- A report naming the PR link, the merge commit, your proof and every decision you made.
- No PR watch left active.

# Entrypoint

## Stage 1: Grant

Read `../full-stop/SKILL.md`. "Full send" grants everything in its Stage 1 and adds one thing:
merging this PR once the Readiness gate passes. The words after "full send" are read the way
that stage reads the words after "full stop". If the trigger was not an explicit "full send",
ask instead of assuming it.

## Stage 2: Prepare

Run full-stop's stages 2–9 as written, using its Readiness gate and Asking the user rules. Come
back here with a **ready** verdict. Waiting for approval, blocked, or a council that did not pass
is not permission to merge.

## Stage 3: Merge

Recheck the live head and the gate. Call `unwatch_pull_request`, then merge with the method the
repository uses; look at its allowed methods and recent merged PRs. When that is unclear or
mixed, squash and merge. With a merge queue or
auto-merge, stay until the host reports the PR merged. Merge through branch protection as
configured, never around it.

## Stage 4: Report

Confirm the host shows the PR merged. Report the PR link, merge commit, proof and decisions. If
someone else merged it first, report what you observed.

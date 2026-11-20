# Council review

Read from `full-stop` Stage 7, when the request asked for a council. `../../council/SKILL.md`
runs each round; this file is the loop around it.

## Before the first round

1. Write the rubric: what a good version of this change looks like in this repository, from what
   you have learned about its conventions, its users and the request. Keep the same rubric for
   every round.
2. With a comparison, collect material on each thing named: screenshots, and notes on how it
   behaves, saved as files the reviewers can open.
3. Take the settings from the request: the target score (9 if none was given), the round cap (5,
   or the count given, or none for "unlimited"), and the comparisons.

## Each round

1. Run one review round with the `council` skill, passing the rubric, any comparison material and
   the target's number of decimal places (one for 9 or 9.5, two for 9.75). The target itself
   stays out of the brief.
2. **Passed** when every voting seat scores at or above the target, no confirmed `blocker` or `should`
   is open, and, with a comparison, every voting seat scores ours above each thing compared.
   Shadow and jester seats do not count. Go back to `full-stop` Stage 8.
3. Otherwise decide what to do with each confirmed finding. Fix the ones that are real defects in
   what was asked for. **Avoid feature creep and push back on overscoped findings.** A reviewer
   who wants more features, more configuration, more abstraction or handling for cases the
   request never raised is asking for a different PR; decline it in a line and record the
   decision with its reason, so the next round's brief carries it. A 20-line change should leave
   review as roughly a 20-line change.
4. Reviewers may propose lint rules. You decide whether each goes in, and the default is yes:
   a rule that catches a class of mistake mechanically keeps later rounds and builders from
   repeating it. Leave a rule out, or take it back out, when it gets in the way of the change
   you judge correct for the problem.
5. With a comparison, read what the reviewers preferred about the other products. Those reasons
   say what to improve next better than the scores do.
6. Size the fixes. A few small ones you make yourself. More than a couple of hundred lines, or
   anything that needs careful checking in the running app, goes to a builder, briefed as in
   `full-stop` Stage 4: every piece of context it needs, and exactly what you want, so it has no
   design to invent.
7. Check the fixes the way `full-stop` Stage 5 does, then commit. Commits made between rounds
   should be `fix` or `chore`. If you are about to write `feat`, stop and ask whether the
   council has talked you into a feature nobody requested.
8. Run the next round.

## When it will not pass

Stop when you reach the round cap, or sooner when rounds have stopped moving the scores and you
are only trading one finding for another. Running out of rounds is not a pass. Stopping and
asking the user is expensive, so first work out why the rounds stalled: if the findings that
will not close come from the approach itself, a different approach is usually worth trying
before you hand the change back. Then choose:

- **Redesign.** Take the findings that would not close back to a design round, as `full-stop`
  Stage 2 does, adding the approach you tried and what kept going wrong with it. Rebuild from
  Stage 3 and start the rounds again with a fresh count.
- **Redesign only the contested part**, when the reviewers accept most of the change and split on
  one piece. Keep both versions as stacked PRs:
  1. Put the part nobody disputes on its own branch and open it as the base PR.
  2. Put the current version of the contested part on a branch cut from that base, and open it
     as a PR against the base.
  3. Hold a design round on the contested part alone.
  4. Launch a new top-level thread with `t3_thread_launch`, on the same model as this thread,
     with `workspaceStrategy` set to a new worktree whose `baseRef` is the base branch and
     `startFromOrigin: false`. Its message is the new design for the contested part and the
     request to build it full stop, as a PR against the base.
  5. Link every PR you opened to its thread with `link_pull_requests`. When the base branch
     changes, `t3_worktree_restack` rebases the branches stacked on it.

  The result is one base PR with two competing PRs on top. Hand all three to the user to pick;
  do not merge either competitor.
- **Hand it back** when the stall is not about the approach (the request is unclear, the
  reviewers want something it never asked for, or what is left is a choice only the user can
  make), or when a redesign has also failed to pass. Report the scores per round and each open
  disagreement from both sides, and ask the user. `full-send` does not merge a change whose
  council did not pass.

---
name: council
description: "Use when the user says 'council' — get independent review of a change, or advice on
  an architecture, plan or question, from a panel of other models. A number after it ('council
  9.5') is the score a review must reach."
metadata:
  type: procedure
---

# Contract

## Input Contract

- The user's request and the thing under council: a diff or PR, or a design question.
- T3 `delegate_task` to reach the panel's models; `harness-delegation` names the launch route.

## Output Contract

- Review: a change every voting seat scores at or above the target, or a stalled report showing
  both sides. Design: one recommended architecture with the dissent stated.
- The tagged notes at the bottom of the final reply. No delegate left running.

# Entrypoint

## Stage 1: Pick the panel

The subject decides the panel. Do not choose members by judgment.

- There is a diff, a PR or an implementation to judge: the **review panel**.
- There is no code yet, and the question is how to build something, which approach to take, or
  what a plan gets wrong: the **design panel**.
- The user named a panel or members: use exactly those, for this run only.

## Stage 2: Seat it

Call `orchestrator_capabilities`, searching by name for anything missing from the short list.
Route each model per `../subagents/model-selection/SKILL.md`: Claude models on the Claude Code
provider, every other model on Pi. A model that is not listed is reported and left out, never
replaced. With fewer than two voting seats, stop and say so. A missing jester changes nothing.

## Stage 3: Brief

Every member of a round gets the same brief and never sees another member's answer. Members are
read-only: no edits, commits, pushes, PR comments or subagents.

**Review brief: as little as possible.** The repository path, the base revision, the one diff
command, the user's request in their own words, and the decisions you made with a line of why
for each. Nothing else. Leave out your exploration, your notes and your belief that it works:
reviewers who explore on their own find what you missed, and reviewers handed your assumptions
inherit them. Ask for this reply:

```
VERDICT: APPROVE or CHANGES
SCORE: <n>/10
APPROACH: sound | wrong - <one line>
F1 [blocker|should|nit] <file>:<line> <claim>. Fix: <suggestion>
```

**Design brief: everything you know.** The problem, the constraints, every relevant file and
finding from your exploration with paths, the options you see and what you have ruled out and
why. These models are expensive; pay for their judgment, not for them to rediscover the
repository. Ask for a recommended architecture, the reasons, the strongest objection to it, and
what they would refuse to approve.

## Stage 4: Run it

**Design.** One round. If the seats agree, that is the recommendation. If they disagree, send
each the other proposals unattributed and ask for a ranking and any veto; take the proposal
nobody vetoes, and the smaller one on a tie. Report the choice and the dissent. Go to Stage 6.

**Review.**

1. Before round 1, fix what you already know is wrong and run the checks. The panel reviews your
   best version.
2. Launch every member in parallel, a fresh delegate each round. Do not edit the checkout while a
   voting member is reading it.
3. The round closes when the voting members have answered. Never wait for a jester; a late jester
   answer is read when it arrives.
4. Check every finding against the code yourself. `blocker` means the intended case is wrong,
   `should` means a real bug callers will hit, anything else is a `nit` whatever it was labelled.
5. A merged seat is one voice: pool its models' findings, and its score is the lower of theirs.
6. **Done** when every voting seat scores at or above the target (9 unless the user gave a
   number) with no confirmed blocker or should open. Go to Stage 6.
7. Otherwise make the smallest fix for each finding you agree with, answer the ones you do not
   with evidence, decline nits in a line, and run another round with the same brief plus what
   changed. Fight scope creep. Do not agree just to end the loop.
8. **Stalled** after three rounds on one architecture, or sooner if a round ends with no fewer
   open findings than the last, or two voting seats say the approach itself is wrong. Go to
   Stage 5.

## Stage 5: Re-architect

The panel has rejected this design, so stop patching it.

1. Commit the attempt and keep it on a branch named `council/<topic>/attempt-<n>`.
2. Take the problem to the design panel with a design brief that adds the attempt's approach and
   the findings that would not close. Ask what about the approach keeps producing them and what
   architecture they would approve.
3. Rebuild from the base revision on the chosen architecture, carrying over only what the design
   panel said to keep. It solves the same request: a new how, never a new what.
4. Start the review rounds again at Stage 4. After two re-architectures, stop: leave the best
   attempt checked out, name the other branches, and show each open disagreement from both
   sides. Running out of budget is not approval. The user decides.

## Stage 6: Report

Cancel any delegate still running. With a PR, put this in its description above the model line,
editing the description rather than commenting; without one, put it in the reply.

```markdown
## Council review

Target: 9.5. Attempts: 2. Rounds on the final attempt: 2.

| Seat | Round 1 | Round 2 |
| --- | --- | --- |
| Sol (6.2 + 6.1) | 7/10 | 9.5/10 |
| Claude Opus 5.5 | 8/10 | 10/10 |
| Muse Ember | no score | 9.5/10 |
```

Never invent a score. End the final reply with the tagged notes, one per line, each starting
with its tag so a later search finds it:

```
sol_comparison: 6.2-sol@<effort> <score> vs 6.1-sol@xhigh <score>. Better: <which, or tie>. Only 6.2 found: <...>. Only 6.1 found: <...>. Both missed: <confirmed findings from other seats>. Wrong: <false findings, by model>.
glm_review: <what GLM raised, which findings held up, which did not, whether it earned its place>
glm_flub: <anything GLM said that was funny or unexpected, quoted>
```

Write `sol_comparison` once per round. Leave `glm_flub` out when there is nothing worth it.

# Panels

Edit these in plain words. Each line is one seat.

## Review panel

- **Sol**, a merged seat: GPT 6.2 Sol and GPT 6.1 Sol. Both review the same brief and count as
  one voice. 6.1 runs at xhigh. 6.2 is under evaluation as its replacement, so each run picks one
  effort for it with `shuf -n1 -e low medium high xhigh`, keeps it for the whole run, and
  records it in `sol_comparison`. Never max.
- **Claude Opus 5.5** at high.
- **Muse Ember** at high.
- **GLM 5.3**, the jester, at high, through OpenCode Go. It is not as sharp as the others. It
  does not vote, is never waited for and gets no score. Treat what it says as a lead: act only
  on what you have confirmed yourself, and write it up in `glm_review`.

Claude Fable 5.2 and GPT 6.2 Astra do not sit on reviews. They cost too much for that work.

## Design panel

- **Claude Fable 5.2** at high.
- **GPT 6.2 Astra** at high. Its best effort is not settled, so say which one you used.

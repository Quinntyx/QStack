---
name: council
description: "Use when a skill or the user asks for a council — how to put one question in front
  of a panel of other models, each working blind, and read what comes back: a design round or a
  scored review round. It does not decide when to hold a council or what to do with the result;
  the skill or request that called it does."
metadata:
  type: procedure
---

# Contract

## Input Contract

- The kind of round: **design** (no code yet: how to build something, which approach, what a plan
  gets wrong) or **review** (a diff, PR or implementation to judge).
- For a design round, the problem and everything you found researching it.
- For a review round, the change, a rubric to score against, and optionally things to compare the
  change with.
- T3 `delegate_task` to reach the panel's models; `harness-delegation` names the launch route.

## Output Contract

- Design: each seat's proposed architecture, its reasons and its strongest objection.
- Review: each voting seat's score, and the findings you confirmed against the code. With a
  comparison, each seat's scores for every thing compared and what it preferred about each.
- The tagged notes for your final reply. No delegate left running.

One call is one round. The caller decides whether to run another.

# Entrypoint

## Stage 1: Seat the panel

Use the review panel for a review round and the design panel for a design round, from Panels
below. If the user named seats, use exactly those for this run.

Call `orchestrator_capabilities` and route each model per
`../subagents/model-selection/SKILL.md`. A model that is not listed is reported and left out,
never replaced. With fewer than two voting seats, stop and say so. A missing jester changes
nothing.

## Stage 2: Brief

Every member gets the same brief, as an ordinary task of its own. The brief does not say that
this is a council, that anyone else is answering, which models are involved, or what score the
change needs. Members are read-only: no edits, commits, pushes, PR comments or subagents.

**Design brief: everything you know.** The problem, the constraints, every relevant file and
finding from your research with paths, how others have built the same thing, the options you see
and what you have ruled out and why. Leave out the design you favor. These models are expensive;
pay for their judgment, not for them to rediscover the repository. Ask for a recommended
architecture, the reasons, the strongest objection to it, and what they would refuse to approve.

**Review brief: as little as possible.** The repository path, the base revision, the one diff
command, the request in the user's own words, the rubric, and the decisions you made with a line
of why for each. Leave out your exploration, your notes and your belief that it works: reviewers
who explore on their own find what you missed, and reviewers handed your assumptions inherit
them. Ask for this reply:

```
SCORE: <n>/10 against the rubric
APPROACH: sound | wrong - <one line>
F1 [blocker|should|nit] <file>:<line> <claim>. Fix: <suggestion>
```

**With a comparison**, add the material on each thing being compared (screenshots, research
notes, links) as files, and ask for the same rubric score for each one, then what the reviewer
liked better about each, in sentences. The reasons matter more than the numbers.

## Stage 3: Run the round

1. Launch every member in parallel, each a fresh delegate. Do not edit the checkout while a
   voting member is reading it.
2. The round closes when the voting members have answered. Never wait for a jester; read a late
   jester answer when it arrives.
3. A merged seat is one voice: pool its models' findings, and its score is the lower of theirs.

## Stage 4: Read the result

**Design.** Lay the proposals side by side: where they agree, where they differ, and what each
objects to. Return that to the caller.

**Review.** Check every finding against the code yourself. `blocker` means the intended case is
wrong, `should` means a real bug callers will hit, anything else is a `nit` whatever it was
labelled. A finding that asks for more than the request asked for is out of scope, not a defect.
Return each voting seat's score and the confirmed findings. Never invent a score.

Cancel any delegate still running. Add the tagged notes to your final reply, one per line, each
starting with its tag so a later search finds it:

```
sol_comparison: 6.2-sol@<effort> <score> vs 6.1-sol@xhigh <score>. Better: <which, or tie>. Only 6.2 found: <...>. Only 6.1 found: <...>. Both missed: <confirmed findings from other seats>. Wrong: <false findings, by model>.
glm_review: <what GLM raised, which findings held up, which did not, whether it earned its place>
glm_flub: <anything GLM said that was funny or unexpected, quoted>
```

Write `sol_comparison` once per review round. Leave `glm_flub` out when there is nothing worth it.

# Panels

Edit these in plain words. Each line is one seat.

## Review panel

- **Sol**, a merged seat: GPT 6.2 Sol and GPT 6.1 Sol. Both review the same brief and count as
  one voice. 6.1 runs at xhigh. 6.2 is on trial as its replacement, so each task picks one
  effort for it with `shuf -n1 -e low medium high xhigh`, keeps it for every round of that task,
  and records it in `sol_comparison`. Never max.
- **Claude Opus 5.5** at high.
- **GLM 5.3**, the jester, at high, through OpenCode Go. It is not as sharp as the others. It
  does not vote, is never waited for and its score is not counted. Treat what it says as a lead: act only
  on what you have confirmed yourself, and write it up in `glm_review`.

Claude Fable 5.2 and GPT 6.2 Astra do not sit on reviews. They cost too much for that work.

## Design panel

- **Claude Fable 5.2** at high.
- **GPT 6.2 Astra** at high. Its best effort is not settled, so say which one you used.

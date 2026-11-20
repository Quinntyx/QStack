---
name: council
description: "Use when a skill or the user asks for a council — how to put one question in front
  of a panel of other models, each working blind, and bring their answers back: a design round,
  a scored review round, or any other question. It does not decide when to hold a council or
  what to do with the answers; the skill or request that called it does."
metadata:
  type: procedure
---

# Contract

## Input Contract

- The question, and what kind it is: a **design round** asks about something not yet built (how
  to build it, which approach, what a plan gets wrong), a **review round** judges a change, and
  anything else is an open question.
- The material the question needs. For a review round, the change, a rubric, optionally things
  to compare it with, and, when the caller needs a score, its number of decimal places (one if
  the caller does not say).
- T3 `delegate_task` to reach the panel's models; `harness-delegation` names the launch route.

## Output Contract

- Each seat's answer in its own words, with the claims you checked marked as holding up or not.
- When a score was asked for, each voting seat's score, and with a comparison its score for
  every thing compared.
- The tagged notes for your final reply.

One call is one round. The caller decides whether to run another.

# Entrypoint

## Stage 1: Seat the panel

Use the design panel for a design round and the review panel for any other question, from Panels
below. If the user named seats, use exactly those for this run.

Call `orchestrator_capabilities` and route each model per
`../subagents/model-selection/SKILL.md`. A model that is not listed is reported and left out,
never replaced. With fewer than two voting seats, stop and say so. A missing shadow or jester
changes nothing.

## Stage 2: Brief

Every member gets the same brief, as an ordinary task of its own. The brief does not say that
this is a council, that anyone else is answering, which models are involved, or what score the
change needs. Members are read-only: no edits, commits, pushes, PR comments or subagents.

The brief is the material and the question. The kind of question decides the material. Gather
what comes from the web with `../web-search/SKILL.md`; its Context.dev route is fine to use here.

**Design round: everything you know.** The problem, the constraints, every relevant file and
finding from your research with paths, how others have built the same thing, the options you see
and what you have ruled out and why. Leave out the design you favor. These models are expensive;
pay for their judgment, not for them to rediscover the repository.

**Review round: as little as possible.** The repository path, the base revision, the one diff
command, the request in the user's own words, the rubric, and the decisions you made with a line
of why for each. Leave out your exploration, your notes and your belief that it works: reviewers
who explore on their own find what you missed, and reviewers handed your assumptions inherit
them. When the caller needs a score, ask for one out of 10 against the rubric, to the caller's
number of decimal places, at least one, and say the precision in the brief: reviewers left to
choose answer in whole numbers, and a target of 9.5 is then out of reach. Say only the
precision, never the target.

**Comparison: matched pairs.** Compare like with like, one item at a time:

1. Go through what changed in ours and list what a reviewer needs to see of it. Cover every
   change and, for an interface, the states that only show on interaction or at the edges:
   hover tooltips, popups and menus, animations, empty, loading and error states. Capture each
   item from the running build into its own file named for what it shows, within what
   `../runtime-verification/SKILL.md` allows for browser work. An animation gets a short
   recording or a few frames.
2. For each item, find each compared product's own version of that feature in the same state,
   and save it beside ours. Run the product when you can; otherwise look in its docs, release
   notes, videos and published screenshots. When a product has no counterpart for an item,
   write that beside the item.
3. Give the reviewers the pairs, and ask for a score for each product and what they liked
   better about each.

**Open question: what an outsider needs to answer it.** Leave out the answer you expect.

End the brief with the question. How to answer it, at what length and in what form, is each
member's choice.

## Stage 3: Run the round

1. Launch every member in parallel, each a fresh delegate. Do not edit the checkout while a
   voting member is reading it.
2. The round closes when the voting members and the shadow seats have answered. A shadow seat
   is always left to finish. Never wait for a jester; read a late jester answer when it
   arrives.
3. A merged seat is one voice: its models' answers go back together under the seat, and its
   score is the lower of theirs.

## Stage 4: Read the answers

Read each answer whole, and check what it claims about the code or other facts you can verify.
Return each seat's answer to the caller in its own words: whole when it is short, quoted where
shortening would lose why a point mattered to that member, with the claims you checked marked
as holding up or not. Then say where the seats agree and where they differ.

When a score was asked for, give each voting seat's score. If a seat's answer does not account
for how far below 10 it scored, report the gap as unexplained. Never invent a score.

A shadow seat's claims go through the same check, with more doubt: assume each one is wrong
until the code shows otherwise. One that holds up is used like any other. Its score is recorded
and never counted.

Cancel any voting delegate still running. Never cancel a shadow seat. A jester that has not
answered is left to finish, and cancelled when the next round starts or the caller is done.
Add the tagged notes to your final reply, one per line, each starting with its tag so a later
search finds it:

```
sol_comparison: 6.2-sol@<effort> <score> vs 6.1-sol@xhigh <score>. Better: <which, or tie>. Only 6.2 found: <...>. Only 6.1 found: <...>. Both missed: <confirmed findings from other seats>. Wrong: <false findings, by model>.
glm_review: <score>. <what GLM raised, which findings held up, which did not, what the voting seats found that it missed, whether it earned its place>
tidepool_review: <the same, for Tidepool Alpha>
glm_flub: <anything GLM said that was funny or unexpected, quoted>
```

Write `sol_comparison` and one `_review` line per shadow seat once per review round. These lines
are the record a shadow seat is judged on later, so say plainly how it did against the voting
seats. Leave `glm_flub` out when there is nothing worth it.

# Panels

Edit these in plain words. Each line is one seat.

## Review panel

- **Sol**, a merged seat: GPT 6.2 Sol and GPT 6.1 Sol. Both review the same brief and count as
  one voice. 6.1 runs at xhigh. 6.2 is on trial as its replacement, so each task picks one
  effort for it with `shuf -n1 -e low medium high xhigh`, keeps it for every round of that task,
  and records it in `sol_comparison`. Never max.
- **Claude Opus 5.5** at high.
- **GLM 5.3**, a shadow seat, at high, through OpenCode Go. It is not as sharp as the others.
  Write it up in `glm_review`.
- **Tidepool Alpha** (`cliproxyapi/tidepool-alpha`), a shadow seat, at max. A new stealth model,
  probably open-weight, so nothing is known yet about how good it is. Write it up in
  `tidepool_review`.

Three kinds of seat:

- A **voting** seat's score counts toward the result.
- A **shadow** seat is a model being tested for a voting seat. It gets the same brief, is left
  to finish every time and is never cancelled. It does not vote and its score is not counted.
  What it says can be used once you have checked it, and should be doubted until then.
- A **jester** seat is there for an extra opinion and nothing more. It does not vote, is never
  waited for and is cancelled when it runs late. Treat what it says as a lead. No model sits
  as a jester at the moment.

Claude Fable 5.2 and GPT 6.2 Astra do not sit on reviews. They cost too much for that work.

## Design panel

- **Claude Fable 5.2** at high.
- **GPT 6.2 Astra** at high. Its best effort is not settled, so say which one you used.

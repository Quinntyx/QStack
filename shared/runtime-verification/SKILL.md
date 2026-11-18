---
name: runtime-verification
description: "Use when fixing bugs, reviewing runtime correctness, investigating repeated failures,
  or verifying code changes against real user flows. Decides how much evidence a change needs and
  what you may use to get it; the harness-verification skill supplies how to exercise the change
  in this harness."
metadata:
  type: procedure
---

# Contract

## Input Contract

- A symptom, a change to verify, or a behavior the user expects to see.
- The repository or running system, and what the task permits you to do to it.

## Output Contract

- What you observed the software do, and for a defect the cause the evidence supports. If you
  could not run something, say which part.
- For a fix: the repair, checked against the flow the user originally reported.
- A report that keeps what you observed apart from what you infer.

# Entrypoint

## Stage 1: Choose the tier

Read the request and the repository's own instructions for running and checking it. Work out
which build, process and configuration are involved and which user flow is affected.

Pick a tier from the ladder below by its triggers. The repository's required checks apply at
every tier.

When investigating a failure, keep an input that reproduces it and trace to the first point where
behavior departs from what was intended before proposing a repair. A review changes nothing. A
fix changes the smallest component that owns the wrong behavior.

## Stage 2: Exercise the change

Load the `harness-verification` skill and follow it, giving it the target, the tier and the
checks the project already has. If its recipe cannot run here, exercise the smallest real
entrypoint the project has and say so.

A change to docs or tests alone needs its own checks, not a made-up runtime flow. A claim that
depends on a real process, network or GPU needs that real thing.

Confirm the running program loaded the build and configuration you changed. Then check the
original flow. A failed check goes back to diagnosis.

## Stage 3: Report

Lead with the result or the finding, then the cause and the evidence that settles it. Say
separately what was changed in source, what was installed, what was restarted and what was
deployed. Name what you could not test.

# Verification ladder

A higher tier keeps the lower tiers' checks and adds to them only where the trigger points.

## Tier 1: Focused

The default for a bounded, understood change with a local way to check it.

- Read the diff you own, run the repository's checks for the changed files, and exercise the
  smallest real entrypoint the change affects.
- For a logic fix, show the regression check failing before the fix and passing after, when that
  is feasible.
- When appearance matters, look at the rendered result. A passing build does not show what a
  screen looks like. One capture of the relevant view is enough.

## Tier 2: Boundary regression

Use this tier when the change touches any of:

- a public or API contract;
- stored state, persistence or a migration;
- a shared asynchronous, process, network or privilege boundary;
- anything security-sensitive;
- installed configuration;
- several surfaces or platforms that interact;
- a regression whose extent is unclear.

Then:

- List the callers and surfaces affected. Test the working path and the failure path across the
  real boundary, plus one nearby path that should be unaffected.
- For an installed update, check each link separately: the source, the selected ref, the
  installed revision, the effective configuration, and whether it is active.
- If the extent is unknown, start here with a short look around. Drop to Tier 1 once the triggers
  above are ruled out.

## Tier 3: Forensic

Use this tier after two failed repairs of the same symptom, for nondeterminism you cannot
explain, for races, for claims about timing, flicker or performance, or when the user asks for
replayable evidence.

- Keep inputs that replay the failure, and the timing, event or state trace around it.
- Tie each experiment to a hypothesis and to what result would confirm or refute it. Stop
  gathering when the symptom, the boundary and the cause are established.
- After a failed repair, diagnose again. The same test run twice tells you nothing new.

# Browser and screenshots

- Use T3 preview tools when the current request asks for browser work or names a page or tab. A
  "full stop" or "full send" grant also supplies that permission for its task. A frontend edit
  alone does not.
- Without that permission, use a capture or runtime facility the repository already provides. If
  there is none, report visual verification as blocked.
- Screenshots the user supplied show what they show. They are not verification of a new build.
- Use real images for claims about appearance, and runtime evidence for claims about interaction.

---
name: harness-verification
description: "Use when a skill names harness-verification, or when exercising a changed runtime
  surface in Pi after runtime-verification has selected the evidence tier. Pi binding: direct
  reproduce, trace, repair and verify, with no native verify workflow."
metadata:
  type: procedure
---

# Contract

## Input Contract

- The target, revision, evidence tier and permitted effects bound by runtime-verification Stage 1.

## Output Contract

- Observed evidence for the original user journey on the final build, or a named blocked boundary,
  returned to runtime-verification Stage 3 for the report.

# Entrypoint

## Stage 1: Reproduce the user journey

1. Exercise the reported entrypoint with the relevant input and environment. Capture its result,
   logs, exit state and elapsed time; use screenshots or traces when those expose the symptom.
2. Follow startup, first use, steady use, cancellation and reconnect paths only where the request
   or observed failure makes them relevant.
3. Record the reproduction command or interaction sequence and preserve the failing input. With
   no runtime available, record that boundary and continue to Stage 2.

## Stage 2: Trace the causal path

1. Follow the actual input through state transitions, process boundaries, asynchronous work and
   persistence until the first divergence from the intended behavior.
2. Form a causal hypothesis and distinguish it from plausible alternatives with a focused
   experiment, trace or source evidence. Reuse existing instrumentation where possible.
3. With an authorized repair and a supported cause, continue to Stage 3. Otherwise return the
   findings and unresolved uncertainty to runtime-verification Stage 3.

## Stage 3: Repair the cause

1. Modify the smallest coherent component that owns the incorrect behavior, preserving the
   requested architecture and observable semantics across affected callers.
2. Add a focused regression check when it captures a durable failure mode, preferring an existing
   test path. Delegated repair follows the subagents skill.

## Stage 4: Verify the repaired runtime

1. Run the decisive check against the repaired build, then repeat the original user journey.
2. Confirm the running process loaded the changed build and the relevant configuration.
3. Use real process, browser, kernel, network or GPU execution for claims that depend on that
   boundary; name the narrower coverage of isolated tests when the real boundary is unavailable.
4. A resolved symptom with passing checks returns to runtime-verification Stage 3. Otherwise
   return to Stage 2 with the new evidence, within the selected tier's bounds.

# Notes

- T3 preview tools need a current browser-work request or a named page/tab. A "full send"/"full
  stop" grant supplies that permission for its task.

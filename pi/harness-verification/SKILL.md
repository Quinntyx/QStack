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

- The target, revision, evidence tier and permitted effects chosen in runtime-verification
  Stage 1.

## Output Contract

- What you observed the original user flow do on the final build, or the part you could not run,
  handed back to runtime-verification Stage 3 for the report.

# Entrypoint

## Stage 1: Reproduce the flow

Run the entrypoint the user reported, with the input and environment that matter. Capture the
result, the logs and the exit state, and a screenshot or trace when that is what shows the
symptom. Keep the command or steps and the failing input.

Follow startup, cancellation, reconnect and similar paths when the request or the failure points
at them. If nothing can be run, say so and go to Stage 2.

## Stage 2: Trace the cause

Follow the input through state changes, process boundaries, asynchronous work and storage to the
first point where behavior departs from what was intended. Form a hypothesis and run one
experiment that separates it from the other plausible causes.

With a cause the evidence supports and a repair the task permits, go to Stage 3. Otherwise hand
the findings back to runtime-verification Stage 3.

## Stage 3: Repair

Change the smallest component that owns the wrong behavior. Add a regression check, in an
existing test path, when the failure is one that could come back.

## Stage 4: Verify the repaired build

Run the deciding check against the repaired build, then repeat the original flow. Confirm the
running process loaded the changed build and configuration. A claim that depends on a real
process, browser, network or GPU needs that real thing; if it is unavailable, say what the
isolated test does and does not cover.

When the symptom is gone and the checks pass, hand back to runtime-verification Stage 3.
Otherwise return to Stage 2 with what you learned.

# Browser permission

T3 preview tools need a current browser-work request or a named page or tab. A "full stop" or
"full send" grant supplies that permission for its task.

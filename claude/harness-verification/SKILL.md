---
name: harness-verification
description: "Use when a skill names harness-verification, or when exercising a changed runtime
  surface in Claude Code after runtime-verification has selected the evidence tier. Claude Code
  binding: the native /verify recipe and its boundaries."
metadata:
  type: guideline
---

# Exercise recipe

- For a changed runtime surface, load native `/verify` through `Skill` when that built-in is
  exposed in the current session. Supply the target/revision, the tier runtime-verification
  selected, existing project checks and the permitted capture route. Native `/verify` owns the
  end-to-end exercise method; reuse its evidence rather than running a second generic workflow.
- Native `/run` launches the project's app when a check needs it running.
- Keep any native run/verify-skill bootstrap within assigned repository-writing authority. Read-only
  or source-only work uses existing instructions and checks without generating project guidance.
- If the native recipe is absent or cannot honor those boundaries, exercise the smallest existing
  project entrypoint directly and record the limitation.

# Boundaries

- A native workflow's completion message is not proof: observe the evidence on the final change.
- T3 preview tools need a current browser-work request or a named page/tab; an evidence requirement
  alone does not grant them. A "full send"/"full stop" grant supplies that permission for its task.

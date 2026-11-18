---
name: model-selection
description: "Use when choosing which model, effort and provider a child agent runs on, or when a
  skill points here for the builder model."
metadata:
  type: guideline
---

# Who does what

Edit these in plain words.

- **The thread's own model** does everything that needs judgment: research, design, reading the
  code that comes back, diagnosing bugs, cleanup and every decision. That work stays in the
  thread unless the user asks to delegate it.
- **The builder** is DeepSeek V4.1 Flash, through OpenCode Go, always at max effort. It
  implements one chunk of work from an explicit brief. It does not research, diagnose, design or
  review.
- **Council seats** are listed in the Panels section of `../../council/SKILL.md`, with their
  efforts.
- A model the user names for a task is used exactly as named, for that task.

# Routing

- With `delegate_task`, Claude models run on the Claude Code provider and **every other model
  runs on Pi** (the Pi T3Main provider), even when the Claude Code provider also lists it.
- Inside a native dynamic workflow in Claude Code, every model runs inside Claude Code, the
  non-Claude ones included, so the workflow keeps running without a break.
- `orchestrator_capabilities` is the live list of what this thread can reach. Call it once per
  thread, and again only after an error or when the user names a different provider. Pass effort
  in `target.options`, for example `{effort: 'max'}`.

# When a model is not listed

Say which model is missing and stop there. Do not pick a substitute, change provider or lower
the effort unasked. The user decides what runs instead.

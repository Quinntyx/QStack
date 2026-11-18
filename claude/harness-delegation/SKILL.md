---
name: harness-delegation
description: "Use when a skill names harness-delegation, or before launching, joining, waiting on
  or cancelling child agents or a delegated review in Claude Code. Claude Code binding: native
  Agent versus T3 delegate_task, native /code-review, and the Claude model boundary."
metadata:
  type: guideline
---

# Launch routes

- Native foreground `Agent` (`run_in_background:false` when exposed) owns in-turn children that use
  this provider, a model this Claude host actually supports, and no extra settings. Use its native
  result/join and cancellation controls; it has no T3 task identity or lifecycle.
- Another provider, requested extra settings, a separate checkout, background work or an explicit
  `delegate_task` request goes through T3 `delegate_task`. Keep native Agent IDs distinct from T3
  taskIds in every record and report.
- Native `/batch`'s automatic worktree/PR orchestration is not the batch route in T3: use managed
  delegates. Use `Workflow` only when the user explicitly asks for one. A native skill grants no
  extra authority.

# Which provider runs a model

- With `delegate_task`: Claude models on the Claude Code provider, **all other models on Pi**
  (the Pi T3Main provider), even when the Claude Code provider also lists them.
- Inside a native dynamic workflow (`Workflow`): every model runs inside Claude Code, non-Claude
  models included. The preference for Pi is not worth breaking the seamless, long-running
  operation of a workflow.

# T3 tools

- T3 MCP tools are deferred: discover them with `ToolSearch` and read the actual schemas. The T3
  route requires the `t3-code` server in the current session. A standalone Claude session without
  it cannot perform managed allocation, T3 secret entry, durable T3 schedules or thread operations;
  report that precise blocker.
- `t3_background_wait([taskId], waiting)` can hold this turn in Working while background children
  run; `waiting:false` clears it. It is for children, not for retained dev servers or watchers.

# Review route

- One independent review uses native `/code-review` through `Skill` when it is exposed and fits the
  task's child and model limits; otherwise one T3 delegated review via the subagents review
  reference. A requested council is the `council` skill instead. Choose one route.
- `--comment` and `--fix` are effects separate from read-only findings; use them only when assigned.

# Model boundary

The maintained model roster and `orchestrator_capabilities` describe T3 targets, not Claude Agent
aliases. Native `Agent` can select only models/options supported by this Claude host; catalog
presence does not grant native access. Keep native model/effort options distinct from T3
`target.options`. Preserve an explicit user model/provider choice or report it unavailable; an
inherited model must still qualify for the assignment. A named external model is staffed through
T3 or reported unavailable, never replaced by Haiku, Sonnet or Opus.

---
name: harness-delegation
description: "Use when a skill names harness-delegation, or before launching, joining, waiting on
  or cancelling child agents in Claude Code. Claude Code binding: native Agent versus T3
  delegate_task, and which models each can run."
metadata:
  type: guideline
---

# Launch routes

- **Native `Agent`**, in the foreground (`run_in_background: false`), for a child that runs in
  this turn on a Claude model this host supports, with no extra settings. Join and cancel it
  with the native controls. It has no T3 task identity.
- **T3 `delegate_task`** for everything else: another provider's model, settings the user asked
  for, a separate checkout, background work, or when the user says `delegate_task`. Keep native
  Agent IDs and T3 `taskId`s apart in your notes and reports.
- A batch of builders goes through T3 delegates, whether they share the checkout or not. Native
  `/batch` makes its own worktrees and PRs, which T3 does not track. Use `Workflow` when the user
  asks for one.

# Which provider runs a model

- With `delegate_task`: Claude models on the Claude Code provider, **all other models on Pi**
  (the Pi T3Main provider), even when the Claude Code provider also lists them.
- Inside a native dynamic workflow (`Workflow`): every model runs inside Claude Code, the
  non-Claude ones included, so the workflow keeps running without a break.

# T3 tools

- T3 MCP tools are deferred: find them with `ToolSearch` and read their schemas. They need the
  `t3-code` server in this session. Without it there is no managed delegation, T3 secret entry,
  T3 schedule or thread operation; say which one you needed.
- `t3_background_wait([taskId], waiting)` keeps this turn in Working while background children
  run; `waiting: false` clears it. It is for children, not for dev servers or watchers.

# Which models native Agent can run

Native `Agent` runs only the Claude models and options this host supports. The roster in
`model-selection` and the `orchestrator_capabilities` listing describe T3 targets, and native
effort options are separate from T3 `target.options`. A model the roster or the user names that
is not a Claude model goes through T3. When it is not available there, say so; Haiku, Sonnet and
Opus do not stand in for it.

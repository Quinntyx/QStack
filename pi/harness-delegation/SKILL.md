---
name: harness-delegation
description: "Use when a skill names harness-delegation, or before launching, joining, waiting on
  or cancelling child agents or a delegated review in Pi. Pi binding: every child goes through the
  t3-code MCP server's delegate_task."
metadata:
  type: guideline
---

# Launch routes

- This Pi profile delegates through the `t3-code` MCP server. Every child is a T3 `delegate_task`,
  including same-provider children; retain its `taskId`. A thread without that server cannot
  delegate: report the blocker.
- Prefer `mode:'async'` for background work. `mode:'wait'` is only for a result this turn cannot
  proceed without, with a real wait boundary; a wait timeout leaves the child live.
- Children are visible in the T3 UI as threads: name them well, keep briefs self-contained, and
  mention a child result by its `link` verbatim.
- Use a "workflow" only when the user asks for one. Pi session commands and shell worktrees are
  not substitutes for T3 allocation.

# Which provider runs a model

- With `delegate_task`: Claude models on the Claude Code provider, **all other models on Pi**
  (the Pi T3Main provider), even when the Claude Code provider also lists them.

# Waiting

- Pi cannot hold a turn open for background children. For a start-only child, follow the returned
  `next` and let the thread go idle; the completion arrives as a wake turn. Do not poll with
  `task_status`, sleeps or watchers.

# Review route

- One independent review is one T3 `delegate_task` with `role:'review'`, briefed per the subagents
  review reference. Choose one route.
- Posting review comments or applying fixes is an effect separate from read-only findings.

# Standing defaults

- Skill rehearsals (create-skill Stage 4) run on provider `pi_pi_t3main`, model
  `opencode-go/glm-5.3-flash`, with normal defaults for every other setting, when that identity is
  listed by `orchestrator_capabilities`. If it is not listed, say so.

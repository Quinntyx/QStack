---
name: harness-delegation
description: "Use when a skill names harness-delegation, or before launching, joining, waiting on
  or cancelling child agents in Pi. Pi binding: every child goes through the t3-code MCP server's
  delegate_task."
metadata:
  type: guideline
---

# Launch route

- Every child is a T3 `delegate_task`, including a child on this same provider. Keep its
  `taskId`. A thread without the `t3-code` MCP server cannot delegate: say so.
- Use `mode: 'async'` for background work. `mode: 'wait'` is for a result this turn cannot
  continue without; when the wait times out the child keeps running.
- Children show up in the T3 UI as threads. Give each a title that says what it is doing, and
  name a child's result by its `link`.
- Use a "workflow" when the user asks for one. Pi session commands and shell worktrees do not
  give a child a T3 checkout.

# Which provider runs a model

- With `delegate_task`: Claude models on the Claude Code provider, **all other models on Pi**
  (the Pi T3Main provider), even when the Claude Code provider also lists them.

# Waiting

Pi cannot hold a turn open for background children. After an async launch, follow the returned
`next` and let the thread go idle. The completion arrives as a wake turn, and that is when you
read the result.

# Standing defaults

- Skill rehearsals (create-skill Stage 4) run on provider `pi_pi_t3main`, model
  `opencode-go/glm-5.3-flash`, with normal defaults for every other setting, when
  `orchestrator_capabilities` lists it. If it is not listed, say so.

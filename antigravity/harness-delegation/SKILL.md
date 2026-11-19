---
name: harness-delegation
description: "Use when a skill names harness-delegation, or before launching, joining, waiting on
  or cancelling child agents in Antigravity. Antigravity binding for T3-managed delegation."
metadata:
  type: guideline
---

# Launch route

- For QStack delegation in T3 Code, use its `delegate_task` tool and retain the returned `taskId`.
  Load the available tool schema before calling it. The shared subagents skill owns the brief,
  model selection and task boundaries.
- Use `isolation: 'worktree'` for a child needing its own checkout. T3 allocates the checkout;
  a shell worktree or a native Antigravity subagent does not create a managed T3 task.
- Use `mode: 'async'` for background work and `mode: 'wait'` when this turn needs the result.
  Follow the returned continuation instructions and read the result when completion arrives.
- Join and cancel through the T3 task controls. Antigravity's native subagent batches have a
  different lifecycle; a batch becoming idle does not prove every child succeeded.
- In a standalone Antigravity session without T3 tools, report that T3-managed delegation is
  unavailable. Installing QStack supplies instructions, not a T3 connection or provider access.

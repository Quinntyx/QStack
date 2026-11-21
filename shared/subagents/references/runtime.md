# T3 `delegate_task`

Read from `subagents` Stage 3 when a child goes through T3. It needs the `t3-code` MCP server in
this session; without it, say so and stop.

## Before the first launch

Call `orchestrator_capabilities` once per thread. It lists the providers, the models each offers,
their options (such as effort) and the runtime modes. Call it again only after an error or when
the user names a different provider. A model or provider that is not listed is unavailable: say
so, and leave the choice of a substitute to the user unless `../model-selection/SKILL.md` defines
a fallback.

## Parameters

`delegate_task(task, target, role, isolation, mode, timeoutMs, interactionMode, runtimeMode,
title, clientRequestId)`. Only `task` is required.

- `task`: the brief. It is everything the child knows.
- `target`: the model and its settings, from `../model-selection/SKILL.md`. `target.model`, and
  `target.options` as a map or a list of `{id, value}`. Given values override inherited ones;
  `{}` or `[]` clears them. A listed model can still fail to start for lack of quota; keep the
  child's actual error.
- `role`: `implementation`, `research`, `review`, `design`, `test` or `general`. A hint for the
  child's setup.
- `isolation`: `'shared'` (the default) runs in your checkout. It suits children that only
  read, and builders that each own different files. `'worktree'` gives the child a new checkout
  on its own branch, cut from your current commit. Uncommitted edits stay behind. The child can
  open a PR from it when its task allows.
- `mode`: `'async'` (the default) returns at once and the result arrives later as a wake turn.
  `'wait'` blocks this turn, for a result you cannot continue without.
- `timeoutMs`: how long a `'wait'` blocks, 10 minutes by default. When it runs out the child
  keeps working and its result still arrives. A deadline for the work itself goes in the brief.
- `runtimeMode`: leave it out unless the user asks for one. A child cannot have a broader mode
  than this thread. `interactionMode: 'plan'` makes the child plan before it edits.
- `title`: the T3 UI lists children by it, so make it say what the child is doing.

## While a child runs

- Follow the returned `next`. Whether this harness can hold its turn open meanwhile is in the
  `harness-delegation` skill.
- The completion wake tells you a child is done. `task_status(taskId)` then reads its `summary`,
  and reading it marks it delivered. Its `workState` is `working`, `waiting_for_children` or
  `result_available`.
- `t3_thread_read(threadId)` reads a child's transcript when the summary is not enough. In a
  reply, name the child by its `link`.
- `task_cancel(taskId, reason)` stops a child, its queue and its PR watches. It is the way to
  stop a child; `t3_thread_interrupt` is for top-level threads.
- `t3_thread_send` steers a running child, and only when the user asked for live guidance.

## After a child finishes

A child is one shot. A re-check, a repair or a retry is a new `delegate_task` whose brief
carries the earlier child's summary, its branch and what was wrong. Keep the failed child's
`taskId` and error in your report.

## Children launched another way

A child started through the harness's own mechanism is joined and cancelled through that
mechanism. The T3 task tools apply to T3 children only.

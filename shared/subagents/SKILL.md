---
name: subagents
description: "Use when delegating work, launching parallel children, coordinating multi-angle
  research or parallel implementation, integrating parallel work, selecting child models, or
  delegating review. Owns the work shape and acceptance; the harness-delegation skill owns how
  this harness launches and joins children."
metadata:
  type: procedure
---

# Contract

## Input Contract

- Requested outcome, acceptance criteria and permitted effects.
- Supplied child counts, parallelism, models, settings and deadlines.
- The `harness-delegation` skill for this harness, and T3 MCP access for managed delegation.
- Verified repository/project binding and exclusive writer ownership where needed.

## Output Contract

- Verified results or a truthful partial outcome with retained resume identities.
- Child identities recorded per launch route, plus relevant revision/evidence records.
- No unassigned publication, installation, merge, new thread or workspace allocation.

# Runtime rules

- Load the `harness-delegation` skill before the first launch. It decides which children this
  harness runs through its own mechanism and which go through T3 `delegate_task`, and it owns the
  join, wait and cancellation controls for each route. Exactly one skill of that name is installed
  per harness; if none is available, report that instead of guessing a launch route.
- A missing managed route is a blocker, not a provider CLI or shell-checkout fallback. Keep the
  parent's mode ceiling: a child never receives broader modes than this thread.
- For T3, call `orchestrator_capabilities` once before the first delegate; repeat only after an
  error or user-named provider change. Put supported settings in `target.options`. Report an
  unavailable named model/provider rather than substituting one.
- T3 owns worktree allocation; the user owns child limits and publication authority. A batch uses
  managed delegates and the independent-implementation reference below.

# Entrypoint

## Stage 1: Select the smallest useful shape

1. Bind outcome, effects and supplied limits. Distinguish total launches from live concurrency;
   reviews/retries count toward the user's cap. Decompose by acceptance outcome, not agent roles
   for their own sake. Give leaves no onward delegation unless explicitly bounded.
2. For model-selection-only work read `model-selection/SKILL.md` and return the plan. For execution,
   choose the launch route using Runtime rules. One assignment needs only lightweight delegation;
   dependent work remains blocked until its inputs are accepted.
3. A single delegated review uses the review route `harness-delegation` names. Comment publication
   and applying fixes remain effects distinct from read-only findings.
4. Continue to Stage 2 with a finite roster and clear acceptance criteria.

## Stage 2: Prepare

1. Check actual runtime, services, task inputs and baseline once. Use `references/runtime.md` and
   model-selection for T3 bindings/settings.
2. Give each child a self-contained brief, owned paths, permitted effects, relevant skill paths and
   a compact expected output. Keep large inputs/artifacts in files rather than pasted prompts.
3. T3 concurrent same-repo writers require the correct bound project and `isolation:'worktree'`;
   allocation starts at the coordinator's committed baseline. Read-only work can share. Explicitly
   prepared distinct repos can each have one exclusive writer with exact source-path ownership.
   A path in a brief does not bind a project, and allocation does not grant a PR or push.
4. Retain identities, limits and input/revision dependencies, then continue to Stage 3.

## Stage 3: Execute

1. Launch each child through its selected route. T3 children use `delegate_task` with a useful
   title/role and a retained taskId. Use returned completion wakes/`next`; do not poll running
   delegates. A wait timeout leaves the child live.
2. For T3, read only the reference selected by the actual work shape:
   - One assignment: `references/delegation.md`.
   - Evidence research: `references/research.md`.
   - Independent/batch implementation: `references/independent-implementation.md`.
   - Dependent integration: `references/dependent-integration.md`.
   - Independent review: `references/review.md`.
3. Record each completion/failure once. Release accepted dependents; keep unrelated results usable.
   Infrastructure/credential failures remain explicit rather than becoming identical retry loops.
4. Continue to Stage 4 when results are ready, or Stage 5 for a start-only/blocked handoff.

## Stage 4: Verify

1. Check evidence, actual changed artifacts and the integrated revision; child summaries alone are
   not proof. Use `../runtime-verification/SKILL.md` and the repository's actual check floor.
2. Use one scoped independent review when needed/requested, not mandatory repeated rounds. Repair
   small findings directly. A new T3 review/re-check is a new `delegate_task`, within the launch cap.
3. Confirm scope and authorized effects. Accepted or budget-limited work goes to Stage 5; a useful
   bounded repair returns to Stage 3. Two failed repairs require renewed diagnosis, not repetition.

## Stage 5: Retain or finish

1. Retain result state, revisions, artifacts, branches/PRs and resume identities proportional to the
   work. Read `references/resumable-state.md` for uncertain side effects or dependent integration.
2. Cancel replaced/unneeded live T3 work with `task_cancel`, not top-level thread interruption.
   Completed task results remain readable; never poll an unfinished task for its final result.
3. Report verified outcomes, blockers and pending effects. Mention T3 children/threads using their
   returned links verbatim.

# Focused entrypoints

`model-selection/SKILL.md` owns model choice, not execution permission. The conditional references
above inherit this skill's scope and runtime rules; they are not standalone advertised commands.

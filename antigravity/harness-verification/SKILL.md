---
name: harness-verification
description: "Use when a skill names harness-verification, or when exercising a changed runtime
  surface in Antigravity after runtime-verification selects the evidence tier. Antigravity
  binding: exercise the project's real entrypoint and inspect its evidence."
metadata:
  type: guideline
---

# Exercise recipe

- Use the target, revision, evidence tier and permitted effects selected by runtime-verification.
  Follow the repository's own checks and reproduce the affected flow through its existing entrypoint.
- Confirm the running program loaded the changed source and configuration. Inspect logs, exit
  status and resulting state; when appearance matters, inspect a capture of the affected view.
- For a defect, trace the first departure from expected behavior, repair its owner, and rerun the
  original flow and its regression check on the final change.
- Use the tools actually exposed in the session. Claude's native verification skills and Pi's
  extensions are not assumed to exist in Antigravity. Report unavailable runtime boundaries
  rather than claiming a source check exercised them.

# Boundaries

- A native subagent's completion message is not verification evidence. Inspect the actual result.
- T3 preview tools require a current browser-work request or a named page or tab. A full-stop or
  full-send grant supplies that permission for its task; a frontend edit alone does not.
- Keep installation, restarts and deployment separate from source-only verification authority.

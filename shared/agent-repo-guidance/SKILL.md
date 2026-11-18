---
name: agent-repo-guidance
description: "Use when creating or repairing AGENTS.md/CLAUDE.md, repository agent guidance,
  verification ladders or recurring-mistake guardrails. Not for ordinary implementation or
  product planning."
metadata:
  type: procedure
---

# Contract

## Input Contract

- A repository, and either a request for agent guidance or a mistake an agent made in it.
- The repository's existing guidance, contribution docs and real commands.

## Output Contract

- Guidance specific to this repository, with pointers that resolve and commands that run.
- Each rule in one place.
- A test or lint rule only for a mistake that has happened and that a machine can detect.

# What goes in a guidance file

Operating rules: what an agent working here must know and cannot quickly find out from the code.
That means unusual domain vocabulary, safety and state boundaries, which doc to read for which
task, the taste rules that matter, and the real commands for checking a change.

A guidance file does not describe how the existing system behaves. The code does that, and a
second copy in prose goes stale and misleads the next agent. Work that is not built yet belongs
in `PLAN.md`, per `../project-plan/SKILL.md`.

# Entrypoint

## Stage 1: Read what exists

Read the existing AGENTS.md and CLAUDE.md in full, the scripts and the stack, and the failure
example if there is one. Keep the repository's own vocabulary.

If the guidance file is managed configuration, find its real source first, with your `edit-config` skill if you have one.
For a new guidance file the user asked for, load the `harness-config` skill and use the bootstrap
it names when there is one; that bootstrap does the first survey and draft, and you edit its
result. Without one, draft from what you read. Existing guidance is repaired in place.

A read-only or draft-only request produces findings or draft text, not a file in the repository.

## Stage 2: Write the repository's own rules

1. Write the operating rules described above. Give the reason for any rule that is not obvious.
   Leave out what an agent would find in a minute of reading the source.
2. Put a rule where it is used: a local reason in a comment, behavior in a test, and a pointer
   from the guidance file to anything longer. Use the docs the repository already has.
3. Use the project's real command names, fixtures and checklists. Pick how much checking a change
   needs from `../runtime-verification/SKILL.md`. Name slow CI-only checks as such, apart from
   the commands to run on changed files.
4. For a mistake that keeps recurring and that a machine can detect, add a check in the test or
   lint framework the repository already uses. Show that a violating case fails and a legitimate
   neighbor passes. A mistake that takes judgment to spot stays as guidance.

## Stage 3: Check and hand off

Read the guidance files together for contradictions and stale paths. Open every link you added
and run every command the guidance recommends. Walk one ordinary task through it to see that it
leads the right way.

Report the paths changed, why, and the checks you ran. Commit or publish only when the task says
to. When the same mistake happens again later, update the rule that owns it.

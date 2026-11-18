---
name: project-plan
description: "Use when planning work before it is built, mostly a new project or a large new
  addition to an existing one: writing or revising PLAN.md. Not for documenting a system that
  already works, and not for agent operating guidance (use agent-repo-guidance)."
metadata:
  type: procedure
---

# Contract

## Input Contract

- The thing to be built, what the user wants from it, and whatever discussion or specification
  they supplied.
- The repository it will live in, if one exists, and its constraints.

## Output Contract

- One file, `PLAN.md`, at the repository root: the design decisions and the work still to do, in
  the order to do it.
- A short summary for the user: the design, the main tradeoffs, the first part to build, and any
  decision that still blocks it.

# What PLAN.md is

`PLAN.md` describes work that has not merged yet, and nothing else. When a part merges, that part
is deleted from the file. When the file is empty it is deleted too, and the plan is done. After
that the project grows one PR at a time with no plan file.

The plan is mostly for a new project or a large new addition, where there is more to build than
one PR holds. It works the same way wherever it is used.

The file never describes behavior that already exists. The code does that, and a second copy in
prose goes stale and misleads the next agent that reads it. So there is no `ARCHITECTURE.md` kept
beside the code: design decisions live in `PLAN.md` while the work they govern is unbuilt, and
leave with it.

# Entrypoint

## Stage 1: Understand what is wanted

Read the request and anything already in the repository. Work out the outcome, how the user will
know it works, the constraints, and the decisions they have already made.

If a missing decision would change the design in a way that is expensive to undo, look for the
answer in what you have. If it is not there, ask one question with the options and your
recommendation, and plan the parts that do not depend on it meanwhile. Record cheaper assumptions
in the plan and move on.

## Stage 2: Choose the design

Research how the pieces will fit: the interfaces, where state lives, what depends on what, and
the external services or libraries the design leans on, checked against their own documentation.
Choose the smallest design that reaches the outcome, and say why its boundaries fit the
constraints.

## Stage 3: Write PLAN.md

1. Start with the decisions: what the system is, its parts and how they talk to each other, and
   the reasons for the choices a reader might question.
2. Then the parts to build, in dependency order. Each part is one PR's worth of work with a
   useful result of its own: what it delivers, what it needs to exist first, and how to check it
   is done.
3. Parts that share no interface can be built in parallel; say which.
4. Use real paths and commands where they exist, and mark proposed ones as proposed.

Keep status out of the file. A part is either still listed, or merged and gone.

## Stage 4: Check it

Read the plan through once as the agent who will build from it. Every outcome the user asked for
has a part that delivers it, the order respects what each part needs, and nothing depends on
something the plan never builds.

## Stage 5: Deliver

Give the user the summary from the Output Contract. If the request was only for a plan, stop
here.

`PLAN.md` may be committed. A plan big enough to span many PRs is worth keeping under version
control, and tracking it is what lets each PR remove its own part.

# Building from a plan

Whoever builds a part removes it from `PLAN.md`, in the same PR when the file is tracked, along with any decision that
only that part needed. The PR that removes the last part deletes the file.

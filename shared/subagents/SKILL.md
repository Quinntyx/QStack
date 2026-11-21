---
name: subagents
description: "Use when handing work to child agents: launching one child or several in parallel,
  splitting an implementation across builders, running parallel research, bringing the results
  back together, or choosing a child's model. The harness-delegation skill says how this harness
  launches and joins children."
metadata:
  type: procedure
---

# Contract

## Input Contract

- The work to hand off, how you will tell it is done, and what the children may do (edit, push,
  open a PR) under the task you were given.
- Any limits the user set: how many children, how many at once, which models.
- The `harness-delegation` skill for this harness. It names the launch route.

## Output Contract

- The children's work, read and checked by you, together in your checkout where it was code.
- No child left running that nobody is waiting for.
- A report of what was done and what was not, naming T3 children by their returned links.

# Entrypoint

## Stage 1: Split the work

Split by outcome: each child gets one piece with a result you can check alone. Use as few
children as the work needs, and stay inside the user's limits. One question is one child.

Give each piece its own files, so that children working at the same time never edit the same
one. Pieces that cannot be separated that way go to one child, or run one after the other. A
piece that needs another piece's result waits until you have accepted that result.

## Stage 2: Write the briefs

The brief is all the child knows. Write it so the child has nothing left to guess:

- the outcome, and the request it serves;
- the files and symbols it owns, and what is out of scope;
- what you already know: decisions made, patterns in the repository to copy, findings by path;
- the commands that check the work;
- anything shared it must not start a second copy of, such as a dev server, a port or a GPU,
  and which child owns it;
- what it may do (edit only, or also commit, push, open a PR);
- what to send back.

Put large inputs in files and give their paths.

## Stage 3: Launch

1. Load the `harness-delegation` skill and use the route it names. For T3 `delegate_task`, read
   `references/runtime.md` once for the parameters.
2. Choose each child's model with `model-selection/SKILL.md`.
3. Children work in your checkout (`isolation: 'shared'`, the default), in parallel, each on
   the files its brief gives it. They see your uncommitted work and each other's as it lands.
4. Use a worktree (`isolation: 'worktree'`) for children that would edit the same files, or for
   competing versions of the same piece. A worktree starts from your last commit, so commit
   first: edits you have not committed do not exist there. T3 makes the worktree; a checkout
   made in the shell, or a path written in a brief, does not bind a child to a project.
5. Within a squash-merged task branch, manage Git however helps you orchestrate cleanly:
   checkpoint before launching children, let children make short one-line commits you can
   cherry-pick or drop, or commit results yourself. How you slice commits inside the branch is up
   to you; if a child commits inside a shared checkout, have its brief tell it to stage only its
   owned paths so it does not sweep up sibling edits.

## Stage 4: Wait

Follow the `next` each launch returns and let the completion wake arrive. A running child is
left alone until then: its status is read after the wake, once.

Cancel a child you have replaced or no longer need with `task_cancel`.

## Stage 5: Read what came back

A child's summary is a claim. Open what it changed or found and check it against the brief: run
the check commands, read the diff, open the cited source. After reading a builder's diff, emit the
`builder_review:` line per `model-selection/SKILL.md`.

When a piece is wrong or incomplete, use Git to roll back or cherry-pick around bad edits rather
than untangling them by hand, scoping any rollback in a shared checkout to that child's owned
files (or waiting until sibling children finish) so you do not clobber parallel work. Fix a small
thing yourself; for anything larger, correct the brief and launch a new child. Children are
one-shot, so the new brief carries the old child's summary, its branch, and what was wrong.

## Stage 6: Bring it together

Work done in your checkout is already together. Merge any worktree branches you accepted, in
dependency order, resolving conflicts toward what the whole change needs. Then check the
combined result once by running it: pieces that each pass alone can still fail together.

Report what was done, what is still open, a 1-2 line builder note if builders ran (per
`model-selection/SKILL.md`), and each T3 child by its link.

# Research in parallel

Give each child one question and ask for its sources: the URL or file and line, the quotation or
code it relies on, and what is still uncertain. Combine the answers yourself, keep disagreements
visible as open questions, and open the sources behind any claim your conclusion rests on.

# Picking up after a lost context

Before launching anything again, find what already exists: `t3_thread_list` and `t3_thread_read`
for children, `t3_worktree_list` for their branches. A child that finished while you were away
still has its result. Before repeating a push, PR or comment, read the remote to see whether the
first attempt landed. Continue unfinished work with a new child whose brief carries the old
one's summary and branch.

# New threads

Delegation uses `delegate_task`. `t3_thread_launch` and `create_threads` make top-level threads,
which are for when the user asks for a thread or a skill the user invoked calls for one.

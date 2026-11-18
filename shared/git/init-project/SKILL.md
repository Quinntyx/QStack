---
name: init-project
description: "Use when initializing a software project or bootstrapping a personal repository,
  including requested Forgejo hosting, GitHub mirroring, tests/CI, and T3 project registration."
metadata:
  type: procedure
---

# Contract

## Input Contract

- The project's name and stack, and what was asked for: a local scaffold, or a hosted repository
  with its visibility.
- The stack's own tools, already installed. For hosting: logged-in Forgejo and GitHub clients
  and a CI runner.
- Any existing source path or partial earlier attempt, which is kept.
- Each hosted effect has to be part of the request. A local scaffold or a plan creates no
  repositories, publishes no branches, and neither moves this thread nor starts a new one.

## Output Contract

- A scaffold that builds, one real test of real behavior, lockfiles and toolchain files, and the
  checks you ran with their results.
- For a hosted project: the Forgejo repository, a server-side GitHub mirror with the same
  visibility, the first commit, `main` and `dev` published, and CI and the mirror both confirmed
  on that commit.
- A T3 project registered on the source path, when registration was asked for.
- No development worktree. T3 makes those later.

# Entrypoint

## Stage 1: Settle what is being made

1. Settle the stack, a one-word project name, the package or module name, where the source goes,
   local or hosted, the visibility, and whether to register a T3 project. The setup section of
   `../SKILL.md` says where source lives by default; a path the user gave wins.
2. Look at the destination and the hosts. Nothing there: continue. A matching partial setup: go
   to Stage 7 and resume it. Something else there: keep it, and go to Stage 7 with the question
   of whether to reuse it.
3. Use the tools that are installed and the stack's official initializer and testing guidance. A
   missing toolchain is something to tell the user to install, not something to install yourself.
4. For hosting, check the accounts, the visibility, the CI runner's label, and that the server
   has mirror credentials. Tokens go through the logged-in clients, never on a command line.
5. Hosted goes to Stage 2. Local-only goes to Stage 3. A request for a plan returns the steps at
   Stage 7 and changes nothing.

## Stage 2: Create the hosting

1. Read `../github-mirror/SKILL.md` and use it for the mirror; it owns that procedure.
2. Create the empty Forgejo repository and the GitHub mirror repository with the same
   visibility, at the addresses in the setup section of `../SKILL.md`. Create each only after
   confirming it does not exist, or reuse a matching empty one.
3. Set up the push mirror with interval `8h0m0s` and `sync_on_commit: true`. Enable Actions on
   the repository.
4. Read the hosting state back. If a write's result is uncertain, read before retrying. Empty
   hosting confirmed: go to Stage 3. Blocked: go to Stage 7.

## Stage 3: Create the source

1. Hosted: clone the empty repository with `t3_project_clone` into the chosen path. Local-only:
   `git init` at the chosen empty path on `main`.
2. Check the origin and that the repository is empty. Point an unborn hosted HEAD at `main` only
   once you have seen it is empty.
3. Run the stack's official initializer in the source root with the real package name, without
   letting it create a nested Git repository. Add ignores, lockfiles and toolchain files, and one
   test that exercises the behavior that was asked for.
4. Add `AGENTS.md` or similar only if the request asked for it, with
   `../../agent-repo-guidance/SKILL.md`.

## Stage 4: Check the scaffold and write CI

1. Run the tests and the format, lint and type checks the stack has. Record each command and its
   result. A run that found zero tests is not a passing suite.
2. For a hosted project, write `.forgejo/workflows/test.yml`. It runs on pushes to every branch,
   feature branches included, and on pull requests into `main` and `dev`.
3. In the workflow, use the runner label you checked, a reproducible dependency install, the real
   test command, action URLs pinned to a reviewed revision, and `persist-credentials: false` on
   checkout. Parse the YAML with a parser that keeps the `on` key as a string, and check the
   actions run on the runner's toolchain.
4. A failing check goes back to Stage 3 or is fixed here. Passing goes to Stage 5. If the task
   stops before committing, go to Stage 7.

## Stage 5: Commit and publish

1. Stage the scaffold's own paths, read the staged diff and run `git diff --cached --check`.
   Commit with the message `chore: initial commit`. Local-only work skips to Stage 6.
2. Push `main` to origin and wait for the CI result on that exact SHA.
3. Create `dev` at the same SHA and push it. A branch ref is not a workspace; make no worktree.
4. Confirm both remote heads and the default branch. Then follow the mirror skill until the sync
   has completed with an empty error and both hosts show the same SHAs.
5. CI or a mirror sync that is missing, failed or still running is reported as pending at
   Stage 7. Confirmed delivery goes to Stage 6.

## Stage 6: Register the T3 project

1. Look for an existing T3 project on the source root and reuse it. When registration was asked
   for, call `t3_project_create` with an explicit `workspaceRoot` and the scaffold's real run
   and test scripts. Its create-a-workspace-for-me mode is for an empty path, not this one.
2. Registering does not move this thread or change its working directory. Keep using absolute
   paths or `git -C`, and report the project as ready.
3. Later work in the project gets its workspace from T3: `t3_worktree_handoff` (after
   `t3_worktree_status`) to move a thread already in the project, `delegate_task` with
   `isolation:'worktree'` for delegates, and `t3_thread_launch` with a `workspaceStrategy` for a
   new thread, when the user asks for one or a skill the user invoked calls for one. A thread
   bound to another project, such as a scratch thread, cannot be moved into this one.

## Stage 7: Report or resume

1. Report the source path, the project identity, the branch refs, the checks, and each effect
   that was requested and done. Mention CI, the mirror and registration only if they happened,
   and name what is still missing.
2. To resume, look at the source, the hosted repositories, the refs, the visibility, the mirror,
   CI and the registered project, then continue from the first stage that is not finished.
   Never repeat a create whose result you have not read.
3. On failure, leave the repositories, worktrees and running jobs as they are and say what the
   next step is. Cleaning up needs its own request, and uses `trash`.

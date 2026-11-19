---
name: git
description: "Use when locating, cloning, forking, initializing, or mirroring repositories,
  selecting branches or worktrees, committing or pushing, or drafting, publishing, updating,
  or responding to repository issues and pull requests."
metadata:
  type: procedure
---

# Contract

## Input Contract

- The repository (a name, a URL or a checkout), the operation asked for, and what the request
  allows you to change.
- Git, and a logged-in client for the host the task is on: Forgejo or GitHub.
- In T3 Code, the project and thread this session is bound to, when worktrees are involved.

## Output Contract

- The repository, checkout, branch and base you worked on, checked against what is really there,
  and the result that was asked for.
- A short report with exact revisions and anything still pending. Work that is not yours is
  left as it was.

# Entrypoint

## Stage 1: Route

Work out the operation, the repository and host, the checkout, the branch and base, and what the
request lets you publish. Then read the child that owns the operation and follow it:

- Starting a new project: `init-project/SKILL.md`.
- Setting up, repairing or migrating a server-side GitHub mirror: `github-mirror/SKILL.md`.
- Drafting, opening, revising or splitting a PR, or answering PR review: `pr/SKILL.md`.
- Researching, drafting, filing, revising or answering an issue: `issues/SKILL.md`.

The children are read through these paths; neither harness advertises them on its own.

Dotfile and application configuration under a manager such as chezmoi is changed at that
manager's source, on that repository's existing checkout, with an `edit-config` skill if you
have one. QStack does not ship one, because it depends on how your dotfiles are managed.

Everything else (locate, clone, fork, branch, commit, push) continues at Stage 2.

## Stage 2: Find the source

1. If the request gives a checkout, look at its origin, branch, worktrees and uncommitted changes.
   Use it where it is; do not move it to fit a naming preference.
2. Otherwise resolve the owner and repository. A bare name is looked up as My setup says. An
   owner or host the user named is used exactly. A network or login failure is not proof that a
   repository does not exist: report it at Stage 6.
3. Look for an existing clone only at the paths My setup names. The directory name `main` does
   not prove the checked-out branch is `main`; read the branch.
4. A request only to locate goes to Stage 6. A clone or fork that does not exist yet goes to
   Stage 3. An existing checkout goes to Stage 4.

## Stage 3: Clone or fork

1. Check the destination is empty or already this repository. Leave anything else there alone
   and report the collision.
2. Clone with T3 `t3_project_clone`, passing the remote and the destination. If T3 cannot do it,
   say so; do not make the checkout in the shell or in a delegate's brief.
3. Fork only when the user asked for a fork. A clone request does not authorize a fork, a
   migration, a mirror, a visibility change, a push or a PR.
4. Check the origin, the default branch and tracking. A fork of someone else's repository keeps
   their repository as `upstream`. A personal repository has one writable `origin`, and its
   mirrors run on the server.
5. Registering a T3 project is separate: use `t3_project_create` only when asked to set the
   project up. It does not move this thread into that project or start a new thread.

## Stage 4: Pick the workspace and branch

1. Read `git status`, the branch and its upstream, and `git worktree list --porcelain`. In T3
   Code, call `t3_worktree_status` before asking for a worktree. A repository you reach by an
   absolute path is not the one this thread is bound to.
2. Keep working in an existing task checkout. Locating, cloning, committing and pushing do not
   need a new branch.
3. For a new branch, follow the repository's convention, and My setup for a personal repository.
   If neither says what to branch from, ask; do not invent a `main` or `dev`, and do not move a
   branch another checkout is using.
4. To move this thread onto a new branch in its own project, use `t3_worktree_handoff` as the
   last call of the turn, with a continuation prompt. It ends the live session.
5. Several agents writing to one repository at once each get a `delegate_task` with
   `isolation:'worktree'`. T3 cuts each checkout from your last commit, so commit first.
   `../subagents/SKILL.md` covers delegation.
6. A new top-level thread is launched with `t3_thread_launch`, with the project and an explicit
   `workspaceStrategy`, when the user asks for a thread or a skill the user invoked calls for one.
7. If T3 cannot provide the workspace, report that. A shell `git worktree add` does not bind a
   T3 thread to it.

## Stage 5: Do the operation

1. Do the operation that was asked for and nothing beside it.
2. Before a commit, read the whole diff you are about to commit, run the checks that apply to
   the changed files, and stage exact paths so changes that are not yours stay out.
3. Commit when the task includes committing; Publication below says when it does. The message
   uses conventional commits (`feat:`, `fix:`, `chore:` and so on) unless the repository uses
   another format, and its wording follows `../deslop/SKILL.md`. No model or agent tool appears
   as a co-author or in any trailer.
4. Before a push, check the remote, the destination branch and that your branch contains the
   remote's commits. If the remote moved, fetch and rebase or merge; keep the other person's
   work. Force-pushing, rewriting history, pruning and merging into the default branch each need
   to be asked for.
5. If a remote write fails or times out, read the remote to see whether it landed before trying
   again.

## Stage 6: Report

Read back the checkout, branch, base and upstream. After a push, compare the remote head with
your local SHA. Report the host, the absolute checkout path, the branch, what was done, the
checks you ran and what is still pending. A local-only branch has no upstream, and that is fine.

# Publication

- A clone or worktree request covers local preparation only. Push when the request asks for
  delivery, or when the repository's convention or My setup says pushing is part of the work.
- A "no commit", "no push" or "local only" instruction always wins.
- Implementing a change does not include opening a PR, filing an issue, posting a comment,
  merging, migrating hosting, changing visibility, deploying, or installing into a live profile.
  Each is its own request.
- Delete files with `trash`, which can be undone. Keep Git configuration changes repo-local.
- Run a command you expect to take more than about 15 seconds in its own detached tmux session,
  and read its output and exit status when it finishes.

# My setup

Edit these in plain words. They are one person's conventions; replace them with yours.

- My repositories live on Forgejo at `git.quinntyx.dev` under `quinntyx`. That is the one
  writable `origin`: `https://git.quinntyx.dev/quinntyx/<repo>.git`.
- Each one is mirrored by the Forgejo server to GitHub at `Quinntyx/<repo>`, with the same
  visibility. The mirror address is `ssh://github.com/Quinntyx/<repo>.git`.
- A bare repository name means `quinntyx/<repo>` on Forgejo first, then `Quinntyx/<repo>` on
  GitHub if Forgejo definitely has no such repository.
- My clones live at `~/docs/src/<repo>/main`. A clone of someone else's repository lives at
  `~/docs/src/<owner>_<repo>/main`.
- My repositories have `main` and `dev`. Feature branches are named `feat-<description>` and cut
  from `dev`.
- In a `dev` checkout of one of my repositories, a request to implement something includes
  committing and pushing it. A requested chezmoi change includes commit, push to `main` and a
  targeted apply; my `edit-config` skill, kept with my dotfiles, owns that.
- The Forgejo CLI is `fj`, logged in as `quinntyx`. Its API token is in
  `~/.local/share/forgejo-cli/keys.json` at `hosts["git.quinntyx.dev"].token`. The API base is
  `https://git.quinntyx.dev/api/v1`. `gh` is logged in as `Quinntyx`.
- The Forgejo server runs as the `forgejo` container defined in `~/docs/host/forgejo`, with its
  data mounted at `/data`.
- Some machines reach Forgejo through a Git URL rewrite to GitHub. Leave such a rewrite in place.

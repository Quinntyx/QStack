---
name: github-mirror
description: "Use when creating or repairing server-side GitHub mirrors of personal Forgejo
  repositories, migrating GitHub-only repos, or consolidating local mirror remotes."
metadata:
  type: procedure
---

# Contract

## Input Contract

- The repositories named, and what to do with each: create a mirror, migrate from GitHub, or
  repair. Their visibility on both sides.
- Git, `fj` logged in to the Forgejo host and `gh` logged in to GitHub. The hosts, owners, token
  location and server container are in the setup section of `../SKILL.md`.
- A private source repository needs credentials the Forgejo server can use to read it, approved
  by the user.
- Repairing the server's own credentials has to be asked for, and needs access to the Forgejo
  container.

## Output Contract

- Forgejo is the source and pushes to `ssh://github.com/{gh_owner}/{repo}.git` from the server,
  with the same visibility on both sides, interval `8h0m0s` and `sync_on_commit: true`.
- A sync that has completed, with an empty `last_error` and the same branch and tag heads on
  both hosts.
- Local clones with one `origin`, the Forgejo one. A real upstream of a fork stays.
- One outcome per repository, naming anything left half-done and any approval still needed.

# Entrypoint

## Stage 1: Take stock

1. For each repository, settle the owner, the name, the visibility, the local checkout and the
   operation. This is for the user's own repositories. Someone else's upstream stays on its host
   and is not a mirror.
2. Check the tools and logins. Call the Forgejo API at the base URL from the setup section,
   reading the token into memory and sending it as an `Authorization: token ...` header. Keep it
   out of command lines, files and the report.
3. Read both repositories, every page of push mirrors, and the refs on both hosts:
   `GET /repos/{owner}/{repo}`, `GET /repos/{owner}/{repo}/push_mirrors`,
   `gh repo view "{gh_owner}/$repo"`, and `git ls-remote --heads --tags` against each host.
4. One side definitely missing: Stage 2. Both exist: Stage 3. A login, network or permission
   failure is reported as that, with nothing changed.

## Stage 2: Create the missing repository

1. **Migrating from GitHub** (only when asked): check the source's visibility first and set the
   destination's visibility explicitly in the Forgejo migration call. The Forgejo server does not
   inherit your local `gh` login. A private source needs approved credentials passed through the
   API in memory, never in a URL or argument. Without them, stop and say what is needed; do not
   route a private repository through a public copy. Check the imported refs and visibility.
   Issues, PRs, releases and settings are migrated only if asked for.
2. **Forgejo only**: create the empty GitHub repository with `gh repo create "{gh_owner}/$repo"`
   and `--private` or `--public` to match Forgejo.
3. Neither exists, or the migration was not asked for: stop and ask what to create.
4. A failed write is reported with what was left behind. On a rate limit, wait as long as the
   host says before retrying.

Then go to Stage 3.

## Stage 3: Reconcile the refs

A Forgejo push mirror force-updates and prunes the destination, so anything that exists only on
GitHub is lost at the first sync. Settle the refs before that.

1. Compare every branch and tag, not only the default branch.
2. If the refs match, or every Forgejo head contains the GitHub history, go to Stage 4.
3. If GitHub has refs Forgejo lacks, and bringing them over was asked for: fetch them into
   temporary refs, check the objects and ancestry, push them to Forgejo with explicit refspecs,
   and run this stage again.
4. If branches have diverged or tags conflict, stop and ask which side wins, keeping both. Two
   branches can share a tip SHA elsewhere and still differ; compare histories.

## Stage 4: Configure the mirror

1. Read the push mirrors again. A mirror that already has the right address and options is
   reused. Wrong options are fixed through the API when repair was asked for. A second or
   conflicting destination: stop and ask which to keep.
2. If there is none, create it: `POST /repos/{owner}/{repo}/push_mirrors` with `remote_address`
   `ssh://github.com/{gh_owner}/{repo}.git`, `interval` `8h0m0s` and `sync_on_commit` `true`. The
   server pushes with the GitHub account key it already holds.
3. Trigger a sync with `POST /repos/{owner}/{repo}/push_mirrors-sync` and check the mirror's
   status a few times with a pause between. Being queued is not being done.
   - Completed with an empty `last_error`: Stage 6.
   - Completed with an error: Stage 5.
   - Still running when you stop waiting: report the sync as pending.

## Stage 5: Fix a failed sync

1. A missing ref, or GitHub refusing to delete its default branch, goes back to Stage 3. A
   credential or host-key error continues here. Any other error is reported as the server gave it.
2. The rest of this stage changes the server. Do it only if server repair was asked for and you
   can reach the container; otherwise stop and ask.
3. **Host key**: get GitHub's SSH fingerprints from GitHub's own documentation over HTTPS and
   compare before adding anything to `/data/git/.ssh/known_hosts`, as the container's Git user,
   keeping the file's owner and permissions. Output from `ssh-keyscan` alone is not verified.
4. **Public key or deploy key rejected**: find which SSH identity the server uses and what it may
   access on GitHub. Mirrors of several repositories need an account-level key, because a deploy
   key works for one repository only. Check `/data/git/.ssh/config` for a line selecting a
   different identity, and fix only the cause you found. Generating or adding an account key
   needs the user's approval.
5. Note the repair and run Stage 4 again. Leave other server credentials and running services
   alone.

## Stage 6: Check, and tidy the local clone

1. Compare all branch and tag refs again, and read back the mirror's address, interval,
   `sync_on_commit`, completion time and error. A mismatch goes back to Stage 3.
2. Look at the local remotes, each branch's upstream, and
   `git config --show-origin --get-regexp '^url\.'` for URL rewrites. `origin` should be the
   Forgejo URL from the setup section. A machine that rewrites that URL to GitHub on purpose
   keeps its rewrite; report the stored URL and the effective one separately.
3. If tidying local remotes was asked for: check Forgejo has every commit each branch's upstream
   points at, set `origin` and the tracking refs, then remove the old personal `github` remote
   and any `upstream` that only pointed at the mirror. Worktrees share the main clone's remotes.
   A fork's real upstream stays.
4. Tool configuration that names the repository as a package source keeps pointing at Forgejo.
   Changing it is a configuration change, made at that configuration's own source.
5. Report the mirror destination, completion time, last error, whether the refs match, the local
   remotes and tracking, and anything pending.

Run a command you expect to take more than about 15 seconds in its own detached tmux session.
Delete files with `trash`.

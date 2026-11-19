---
name: pr
description: "Use when drafting, opening, revising, or splitting pull requests, or responding
  to PR review feedback with commits, descriptions, or comments."
metadata:
  type: procedure
---

# Contract

## Input Contract

- What to do with a PR, and the repository or PR URL, the branch or diff, and the task it serves.
  The PR may be anyone's, in anyone's repository.
- Git, and `gh` for GitHub or `fj` or the Forgejo API for Forgejo, logged in.
- What the request allows:
  - "Open" or "create" a PR means publish it.
  - "Draft" or "write" the PR text means return the text without publishing. Opening a draft PR
    on the host is a publication and has to be asked for.
  - "Reply" means post that reply.
  - Implementing a change does not include opening a PR or posting review comments, and merging
    is always a separate request.

## Output Contract

- A title and body that start from the problem and match the whole diff, what was verified and
  what was not.
- The destination repository, head, base and draft state, and whether it was published.
- For review follow-up: a reply on the PR giving the finding, the change, the commits, the
  checks and what is still open, readable by someone who never saw the agent conversation.

# Entrypoint

## Stage 1: Pin down the operation

1. Decide what is being produced and whether it is published. If the request is ambiguous, keep
   it as an unpublished draft.
2. Read the repository, the branch and any existing PR, and check the PR's base and head against
   the real refs. Follow that repository's contribution rules, whoever owns it.
3. Settle the base, head and draft state from the request, the existing PR and the repository's
   rules. If a ref that matters cannot be settled, stop and ask for that one choice.
4. Read the contribution instructions, the PR template, and every page of review threads and
   timeline. On GitHub that means issue comments, pull review comments, reviews and the GraphQL
   review threads, paginated. A summary only tells you where the discussion is.

## Stage 2: Read the change

1. Read the full diff with `git diff "$base...$head"`, not the commit subjects. Account for every
   behavior change, flag, default, signature change and control-flow change.
2. Work out why the change exists from the task, the discussion and what the code does. If the
   intent is missing and matters, ask one question.
3. Run the smallest checks that cover the change and read their output. Keep apart what you
   observed, what you infer and what nobody verified.
4. Review fixes are made in the checkout the task gave you, under the commit and push rules of
   `../SKILL.md`.
5. A request to split goes to Stage 2A. Everything else goes to Stage 3. A failing check is
   repaired if that is in scope, and reported if not.

## Stage 2A: Split

1. Divide the whole diff by outcomes that are each useful alone, not by file or commit count.
   Find what the parts share, and whether they can be independent PRs or need a stack.
2. A request for a plan or a draft returns the split plan and the proposed PR texts and goes to
   Stage 5. Splitting does not include rewriting published history or force-pushing unless that
   was asked for.
3. To carry the split out, keep the original branch and SHA, and build each part in a workspace
   T3 allocated.
4. Check each part on its own base, with its own tests. Then check that the parts together still
   do what the original did, with no hunk dropped or duplicated.
5. Run Stages 3 to 5 for each part with its own base, head and text, and report the order they
   depend on each other in.

## Stage 3: Write it

Read `../../deslop/SKILL.md` first. It covers how the text reads; the steps below say what goes
in it.

1. Follow the repository's template and its vocabulary. The title follows the repository's commit
   convention. Where PRs are squash-merged under conventional commits, the title is the
   conventional subject line (`fix: stop the cache evicting pinned entries`), because it becomes
   the commit. Otherwise write a plain sentence-case title naming the symptom or the result.
2. Start the body with what breaks, when, and why it matters. Then the mechanism and the scope,
   then what was verified and the limits that matter. Two to four paragraphs is usual; use
   bullets for parallel changes; keep the template's required sections.
3. Say what is partial and what is unverified. Claim that behavior is unchanged only with
   evidence. The body is about the change: leave out how the work was organized and what the
   agent did along the way.
4. A review reply answers the concern first, then gives the finding, the change with its commit
   references, the check, and what is still open. Attribute quotations correctly.
5. For a PR an agent built, end the description with one line naming the models that did the
   work, and the review if there was one: "Built with Opus 5.5 orchestrating DeepSeek V4.1
   Flash, reviewed by a council of 6.1 Sol, 6.2 Sol, Opus 5.5 and GLM 5.3 with a final score of
   9.83." Name the models that actually ran; the score is the mean of the voting seats' final
   scores. This line is the only mention of a model or agent tool: no model appears as a
   co-author or contributor, and no "Generated with" line, tool badge or other attribution goes
   in the description or in a commit trailer.
6. If the request publishes, go to Stage 4. A draft goes to Stage 5.

## Stage 4: Publish or revise

1. Read the PR and its comments again, so you keep edits people made meanwhile and do not post a
   duplicate. Check the repository, base, head and draft state once more.
2. Create on GitHub from files: `gh pr create --repo "$repo" --base "$base" --head "$head"
   --title "$title" --body-file "$body_file"`, adding `--draft` only when a draft PR was asked
   for. On Forgejo use `fj` or `POST /repos/{owner}/{repo}/pulls` with explicit head and base;
   check how that host marks a draft before relying on it.
3. To revise, edit the existing title and body; do not open a second PR. Post a review reply to
   the thread it answers.
4. Timeline comments on GitHub: `gh pr comment "$number" --repo "$repo" --body-file
   "$body_file"`. On Forgejo: `POST /repos/{owner}/{repo}/issues/{number}/comments`, and
   `PATCH /repos/{owner}/{repo}/issues/comments/{id}` to edit a comment you posted. Use the
   host's logged-in client and keep tokens out of commands and output.
5. If a write fails or times out, read the PR to see whether it landed before trying again.

## Stage 5: Check and report

For something published, read it back from the host: repository, base, head, title, body and
draft state. Return the URL and a line on the outcome. For a draft, return the full text and say
it is unpublished. Either way name the checks that ran and what is still unverified.

---
name: issues
description: "Use when researching, drafting, filing, revising, or responding to repository
  issues, bug reports, feature requests, or duplicate reports."
metadata:
  type: procedure
---

# Contract

## Input Contract

- A report, a question, an issue URL, a failure you can reproduce, or a feature request, in any
  repository, whoever owns it.
- Read access to the repository and its discussions, and a logged-in client for any write.
- What the request allows:
  - "File", "open", "create", "submit" or "post" an issue means publish it.
  - "Reply" or "respond" means post that reply.
  - "Draft", "word", "review", "explain" or "how do I file" means return text without
    publishing. So does "I'd like to file this someday".
  - Editing an existing issue, changing labels, closing, and deleting comments each have to be
    asked for. Filing a new issue includes setting the labels it warrants.

## Output Contract

- A draft, or a published issue or reply read back from the host, in the right repository.
- A neutral title that names the symptom, and a short body that fills in the repository's
  template.
- For a bug: the smallest reproduction, expected and actual behavior, and the version and
  environment. An unfinished reproduction or an uncertain diagnosis is labelled as such.
- For a duplicate: a pointer to the existing issue, and a comment there if you have new evidence
  and were asked to post.

# Entrypoint

## Stage 1: Pin down the operation

Decide whether this is a new issue, a reply, a revision or research, and whether it is published.
If the request is ambiguous, keep it as a draft. Check you can read the repository, and write to
it if you will need to. If you cannot, go to Stage 6 with the draft and say what access is
missing.

## Stage 2: Read the repository

1. Read the contribution guidelines, the security policy, the issue templates and forms and their
   configuration. Use the support channel the project names and fill in every field its template
   requires. A security vulnerability goes through the project's private disclosure channel:
   write a private draft and go to Stage 6.
2. For an existing issue, read the whole body and every page of comments and timeline. On GitHub:
   - `gh issue view "$number" --repo "$repo" --json title,body,author,labels,state,url`
   - `gh api --paginate "repos/$repo/issues/$number/comments?per_page=100"`
   - `gh api --paginate "repos/$repo/issues/$number/timeline?per_page=100"`

   Read the reviews and open threads of any linked PR that bears on it. Note who said what and
   when, what maintainers answered, and what was later corrected. A truncated view only tells
   you where the discussion is; fetch the rest before concluding anything.
3. List the repository's labels (`gh api --paginate "repos/$repo/labels?per_page=100"`) and issue
   types, and look at how recent issues are titled and written.

## Stage 3: Check the evidence and look for duplicates

1. Search open and closed issues and PRs for the symptom, the error text, the component and the
   mechanism. `gh issue list --repo "$repo" --state all --search "$query"` finds candidates but
   is not a complete list. To sweep every open issue, paginate
   `gh api --paginate "repos/$repo/issues?state=open&per_page=100"` and drop the PR records.
2. Read each candidate in full, as in Stage 2. It is a duplicate when the evidence and the failure
   mechanism match. Similar wording is not enough, and two causes get two reports.
3. Build the smallest reproduction: the exact version or commit, the environment and inputs, steps
   that run, the expected result, the observed result, and the shortest trace that shows it. Run
   it if you can. Link sources the readers can open, pinned to a commit. Keep credentials, private
   session material and unrelated logs out.
4. Keep what you observed apart from the likely cause and from a proposed fix. Check claims about
   the source against the current code. A reproduction you did not run is marked as not run. If
   essential evidence is missing, ask for it or write the draft as explicitly incomplete; do not
   fill the gap with invented detail.
5. A duplicate that already records everything you have goes to Stage 6 with its link. A
   duplicate you can add evidence to, and a new report, go to Stage 4.

## Stage 4: Write it

Read `../../deslop/SKILL.md` first. It covers how the text reads; the steps below say what goes
in it.

1. Write a neutral sentence-case title that can be understood without opening the issue. A bug
   title describes the symptom; a feature title names the capability wanted. Use the prefixes and
   vocabulary the repository uses. Keep a guessed diagnosis out of the title.
2. Follow the template. A bug body starts with the failure and what triggers it, then the
   reproduction, expected and actual behavior, version and environment, and the evidence. A
   feature body gives the problem, the outcome wanted, the scope and the alternatives. A short
   report stays short.
3. Write for the maintainers in plain prose and the project's own terms. Include code, traces and
   source locations where they let someone reproduce the problem or back a claim. Leave out what
   the agent did and any private conversation.
4. A reply answers the question or correction first, then gives the new evidence, what it shows
   and what is still uncertain. Link a stable artifact in place of a long pasted log.
5. To revise an issue the user's own agent drafted, fix the title and body in place and keep the
   human discussion. Text someone else wrote stays theirs: put a correction in a reply.
6. Add only existing labels and types that the report supports, and few of them. Some labels
   trigger automation; check before adding one.
7. If the request publishes and the evidence is in hand, go to Stage 5. A draft, missing evidence
   or unclear permission goes to Stage 6 with the text and the open question.

## Stage 5: Publish or update

1. Read the destination and the issue again. For a new issue, repeat the duplicate search; a
   duplicate found now goes back to Stage 4 as a reply. For a revision, keep edits people made
   meanwhile.
2. Create on GitHub from a file: `gh issue create --repo "$repo" --title "$title" --body-file
   "$body_file"`, with `--label` for each label that is warranted. Issue types go through the
   API where the repository supports them.
3. Reply on GitHub with `gh issue comment "$number" --repo "$repo" --body-file "$body_file"`.
   Revise an issue with `gh issue edit "$number" --repo "$repo" --title "$title" --body-file
   "$body_file"`. To revise a comment, confirm its ID and that it is yours, and target that ID.
4. On Forgejo use `fj`, or `POST /repos/{owner}/{repo}/issues` to create,
   `POST /repos/{owner}/{repo}/issues/{number}/comments` to reply, and
   `PATCH /repos/{owner}/{repo}/issues/{number}` to revise, sending label IDs. Use the host's
   logged-in client and keep tokens out of commands and output.
5. If a write fails or times out, read the destination to see whether it landed before trying
   again, and keep the draft text. A permission or API error goes to Stage 6 with the draft.

## Stage 6: Check and report

For something published or edited, read it back from the host: repository, number, URL, title,
body or reply, labels and author. Report the URL and a line on the result, with the limits of the
evidence. For a draft, return the full title and body or reply and say it is unpublished. For a
duplicate, return the existing URL and whether you posted to it.

Run a command you expect to take more than about 15 seconds in its own detached tmux session.

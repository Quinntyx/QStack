# Council briefs

A delegate gets no history: each brief is its whole world. Fill the angle-bracket fields and send
the same text to every member of the round.

## First-round brief

```
You are one reviewer on a council. Review only: do not edit, commit, push, comment on PRs or
start subagents. Other reviewers work independently; you will not see their output.

Repo: <abs path>   Base: <sha>
Intent: <one or two sentences>
Out of scope: <what this change deliberately leaves alone>
Checks run: <commands and results>
See the change: <the one diff command>; git status --short (read untracked files too).
<Design decision and the acceptance criteria the council set, when this follows a design round>

Read the surrounding code. Find bugs, broken callers and mismatches with the intent. Skip style
unless it hides a bug. Hold the change to the smallest thing that satisfies the intent, and flag
code, tests or guards the intent does not need. If you believe the approach itself is wrong, say
so plainly and say what approach you would accept.

blocker = the intended case is wrong. should = a real bug callers will hit, inside the intent.
nit = everything else.

Reply in exactly this shape:
VERDICT: APPROVE or CHANGES
SCORE: <n>/10
APPROACH: sound | wrong - <one line>
F1 [blocker|should|nit] <file>:<line> <claim>. Fix: <suggestion>
F2 ...
```

## Follow-up brief

Send the first-round brief again, then:

```
This is round <n>. Prior findings and what happened to each:
<id> fixed: <what changed>
<id> disagree: <reason with file:line, test or output>
<id> declined: <one line>
Change since the last round: <diff command or summary>

Review only the open ids and the code that changed. Mark each prior id `resolved` or
`still open: <reason>`, add new findings only for changed code, then give VERDICT, SCORE and
APPROACH as before.
```

For a model that did not raise a finding in the previous round, include the finding anyway: every
member reviews the same ledger.

## Design brief

```
You are one member of a council that has reviewed <n> rounds of a change without approving it.
Patching is over; the council is choosing a different architecture. Read only: do not edit.

Repo: <abs path>   Base: <sha>
Problem to solve: <the user's request, unchanged>
Constraints and out of scope: <...>
Attempts so far:
  attempt-<k> (branch council/<run>/attempt-<k>): <approach in two lines>; open findings: <ids>
Open findings: <id, severity, claim, both sides>

Answer in this shape:
ROOT CAUSE: <what about the attempted approach makes these findings keep coming back>
ARCHITECTURE: <the design you would approve: components, data flow, what is deleted; the smallest
  design that solves the stated problem at its root>
SALVAGE: <what from the attempts should be carried over, by path>
ACCEPTANCE: <the checks you will hold the result to>
RISKS: <what could still go wrong with your design>
```

## Ranking brief

Used only when the voting seats' architectures conflict. Label the proposals A, B, C without
saying who wrote which.

```
The council produced these candidate architectures for <problem>:
A: <proposal>   B: <proposal>   C: <proposal>
Read only. Rank them best first for solving the stated problem with the least machinery, and
name any you would refuse to approve.
RANK: <e.g. B, A, C>
VETO: <letters or none> - <reason>
```

## Consult brief

For a question, plan or opinion, send the request and its context with: "Answer independently and
read-only. Lead with your recommendation, then the reasons, the strongest objection to your own
position, and what would change your mind."

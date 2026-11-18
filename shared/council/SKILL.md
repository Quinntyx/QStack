---
name: council
description: "Use when the user says 'council' — get review or feedback from the configured roster
  of models, with paired models merged into one seat and compared, jesters as non-blocking
  advisors, bounded review rounds, and a re-architecture when the council will not converge."
metadata:
  type: procedure
---

# Contract

## Input Contract

- The user's request and the thing under council: a diff, PR, plan, design or question.
- `roster.yaml` beside this file, or council members the user names for this run.
- The `harness-delegation` skill and T3 `delegate_task` to reach other providers' models.
- For a converging run: authority to change the implementation, and a known base revision.

## Output Contract

- Consult: one round of independent responses, synthesized into findings, disagreements and next
  steps. Nothing is changed.
- Converge: an implementation every voting seat approves, or an honest stalled report after the
  attempt budget, with every abandoned attempt preserved on its own branch.
- A ledger for the run and one comparison record per round in the council log.
- No delegate left running, and no scope added that the user did not ask for.

# Entrypoint

## Stage 1: Frame

1. Choose the mode. **Consult** when the user wants opinions, feedback on a plan, or a review of
   work that is not yours to change. **Converge** when the user wants their change taken through
   the council, including under "full send" or "full stop". A bare "council" on your own
   in-progress change is Converge.
2. Before a Converge review, address outstanding PR comments, fix issues you already know about
   and run the covering checks. The council reviews your best version, not a draft with known
   holes. If the user wants the implementation discarded, skip fixes to code being replaced.
3. Fix the subject for the whole run: repository, base revision, one diff command, a one or two
   sentence intent and what is out of scope. Pick a run id `<date>-<slug>`.
4. Run `bin/council-log path` and create `<path>/<run>/ledger.md`. The ledger holds the frame,
   the resolved roster, every finding by stable id with its outcome, and each attempt's summary.

## Stage 2: Seat the council

1. Read `roster.yaml`. Members the user names for this run replace or adjust it for this run only.
2. Call `orchestrator_capabilities` (search by name for models missing from the short list) and
   resolve every model to a provider, model id and effort option. Record them in the ledger.
3. An unresolvable model is reported, never substituted. A seat keeps its remaining models; a seat
   with none is vacant. With fewer staffed voting seats than `min_voting_seats`, stop and report.
   A vacant jester seat is noted and the run continues.

## Stage 3: Run a round

1. Launch every member in parallel, one read-only delegate per model, through the launch route in
   `harness-delegation` (`role:'review'`, async, a fresh delegate each round). Every member gets
   the same brief from `references/briefs.md`: the first-round brief in round 1, the follow-up
   brief afterwards. Members never see each other's output.
2. Leave the reviewed checkout untouched while a voting member is still reviewing it. As each
   result arrives, check its findings against the code and decide what you would fix.
3. The round closes when every voting model has answered. Jesters are never waited for: a jester
   result that arrives in time joins this round, a late one joins the next, and one that never
   arrives is recorded as absent. A failed or timed-out voting delegate is relaunched once; a
   second failure makes that model absent for the round, which is not approval.
4. Verify every finding yourself and set its severity: `blocker` (the intended case is wrong),
   `should` (a real bug callers will hit, inside the intent) or `nit` (everything else, including
   other paths, rare cases and small costs, whatever label it arrived with). Mark each
   `confirmed` or `refuted` with evidence.
5. Merge each seat into one voice. Deduplicate its models' findings by location and claim. The
   seat's verdict is APPROVE only when no confirmed blocker or should from any of its models is
   open. A jester's confirmed finding is adopted into the ledger as the coordinator's own; its
   unconfirmed ones are dropped.
6. Record the round with `bin/council-log record` (see Council log). For a seat with several
   models, say which did better this round and why, and what each missed.
7. Consult ends here: go to Stage 6. Converge continues to Stage 4.

## Stage 4: Converge or stall

1. **Converged:** every voting seat approves the current diff and you have no concern of your own.
   Go to Stage 6.
2. **Stalled:** any of these. Go to Stage 5.
   - `rounds_per_attempt` rounds have run on this attempt without converging.
   - A round ends with no fewer open blockers and shoulds than the round before it.
   - The same finding is still disputed after you and a voting seat have each replied twice.
   - Two or more voting seats object to the approach itself rather than to details of it.
3. **Otherwise:** answer the findings. Agree: make the smallest fix, preferring to delete or
   narrow over adding a lock, cache, helper or option; add one focused test that fails without
   it when the intent needs one. Disagree: say why with evidence. Nit or out of scope: decline in
   one line and list it as a follow-up. Re-run the checks, update the ledger, and run the next
   round at Stage 3. If review grew the diff, cut before the next round. Fight scope creep; do
   not agree just to end the loop.

## Stage 5: Re-architect

The council has rejected this architecture, so patching it further is wasted rounds.

1. If `max_attempts` attempts have been made, go to Stage 6 as stalled.
2. Preserve the attempt: commit its owned paths locally and create
   `council/<run>/attempt-<n>` at that commit. Write its approach, final scores and open findings
   into the ledger.
3. Hold a design round. Send every member the design brief from `references/briefs.md` with the
   frame, each attempt's approach and the open findings. Each voting seat names the root cause of
   its objections, the architecture it would approve, what is worth salvaging and the acceptance
   criteria it will hold the result to. Jester proposals are input, as before.
4. Choose the architecture. If the voting seats' proposals agree, adopt that one. If they
   conflict, send all proposals back unattributed with the ranking brief; adopt the one no voting
   seat vetoes with the best total rank, and on a tie the smallest. Record the choice, the
   reasons and any dissent in the ledger. The new architecture solves the same request: a design
   round changes how, never what.
5. Start the new attempt from the base, not on top of the rejected one: restore the owned paths
   to the base revision with a forward commit, then build the chosen architecture, bringing over
   only what the design round named as salvage. Prove it with the covering checks.
6. Reset the round counter and return to Stage 3 with the first-round brief plus the design
   decision, so the seats review against the criteria they set.

## Stage 6: Report and clean up

1. Cancel any delegate still running (`task_cancel`), jesters included.
2. Stalled after the budget: leave the working branch on the attempt with the fewest open
   blockers and the highest lowest voting score, name the other attempt branches, and show each
   unresolved disagreement with both sides in two or three lines. Running out of budget is not
   approval. The user decides.
3. If the work ends in a pull request, put the results in its description, above the model and
   harness line. Edit the description rather than posting a comment. With no PR, put the same
   results in the final reply.

   ```markdown
   ## Council review

   Attempts: 2 (re-architected once: per-request cache replaced by passing the session down)
   Rounds on final attempt: 2

   | Seat | Model | Round 1 | Round 2 |
   | --- | --- | --- | --- |
   | sol | GPT 6.2 Sol | 7/10 | 9/10 |
   | sol | GPT 6.1 Sol | 8/10 | 9/10 |
   | claude | Claude Opus 5.5 | 6/10 | 9/10 |
   | muse | Muse Ember | no score | 8/10 |
   ```

   Jesters are not listed. A model that gave no score is `no score`; never invent one.
4. Report: mode, roster as seated and anything vacant, attempts and rounds, fixed and declined
   findings with reasons, the paired-model comparison for each multi-model seat, what the jesters
   contributed, and the ledger path.

# Council log

`bin/council-log` appends one JSON record per round and summarizes across runs. It needs
`python3` and writes under `${XDG_STATE_HOME:-~/.local/state}/qstack/council/`.

```sh
bin/council-log path                 # print the log directory
bin/council-log record round.json    # validate and append one round ("-" reads stdin)
bin/council-log summary              # per-model totals across every recorded round
```

A round record. `raised`, `confirmed`, `refuted`, `unique` and `missed` count blockers and shoulds
only: `unique` is confirmed findings no other member raised that round, `missed` is confirmed
findings from other members that this model did not raise. `better` and `why` are for seats with
several models; use `"tie"` when neither was clearly better.

```json
{"run": "2026-11-18-session-cache", "repo": "/abs/path", "subject": "PR #12",
 "mode": "converge", "attempt": 1, "round": 1, "outcome": "continue",
 "seats": [
  {"seat": "sol", "tier": "voting", "verdict": "CHANGES",
   "better": "gpt-6.2-sol", "why": "found the stale-read race; 6.1's only unique finding was a nit",
   "models": [
    {"model": "gpt-6.2-sol", "effort": "high", "verdict": "CHANGES", "score": 7,
     "raised": 4, "confirmed": 3, "refuted": 1, "unique": 2, "missed": 0},
    {"model": "gpt-6.1-sol", "effort": "high", "verdict": "APPROVE", "score": 8,
     "raised": 1, "confirmed": 1, "refuted": 0, "unique": 0, "missed": 2}]},
  {"seat": "glm", "tier": "jester", "verdict": null,
   "models": [{"model": "glm-5.3", "effort": "high", "verdict": null, "score": null,
     "raised": 6, "confirmed": 1, "refuted": 5, "unique": 1, "missed": 2}]}]}
```

`outcome` is `continue`, `converged`, `rearchitect`, `stalled` or `consult`. A model that did not
answer is recorded with `"absent": true` and no counts.

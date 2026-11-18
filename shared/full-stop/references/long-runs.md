# Long runs

Read from `full-stop` when the task includes a run that takes longer than you can sit through
in one turn: model training, a long benchmark, a large evaluation or data job.

## Before you launch

1. You launch the run yourself. Builders may have written the code around it, but the launch
   command, its configuration and everything that happens once it is running are yours.
2. Prove the pipeline on something small first: a few steps of training, a handful of benchmark
   cases, with checkpointing, logging and the final write-out all exercised. A crash in the
   first minute of a short run costs a minute.
3. Write down what a healthy run looks like, before there is a curve to rationalize: the numbers
   you will watch, roughly where they should be at which point, how long the run should take,
   and what would make you stop it.
4. Start it detached from your turn, so it keeps running when the turn ends, with its output
   going to a log file you can read later.

## Checking back

A run you are not looking at can fail for hours before anyone notices. Set up a recurring check
with `schedule_task`: an interval schedule, bound to this thread, whose prompt says what is
running, where its logs and checkpoints are, and what healthy looks like. Then call
`t3_background_wait` with the schedule's ID and end the turn. That keeps the thread shown as
Working for as long as the schedule lives, instead of looking finished between checks; the wait
carries over from one check to the next, so it is set once. Outside T3, use the harness's own
scheduler.

Pick the interval from how long the run should take and how fast you would have to act if it
went wrong:

| Interval | When |
| --- | --- |
| 5 minutes | Stopping late loses something. A training run that starts to diverge has to be stopped before the last good checkpoint rotates out of the ones kept on disk. Also the first stretch of any run, when most failures happen. |
| 15 minutes | The usual choice: a run of a few hours, where a late stop wastes compute and nothing else. |
| 1 hour | A run of many hours or days that is stable and loses nothing but time if it is stopped late. |

Change the interval when the run moves from one of these cases to another.

Each time you wake:

1. Look at the run: is the process alive, is it advancing at the expected rate, are the numbers
   where you said they should be, is there disk left for the next checkpoint.
2. If everything is fine, end the turn. Do not start other work on the same machine that
   competes with the run.
3. If it has gone wrong, stop it while the good state still exists, and keep that checkpoint
   and the logs. Work out why yourself, fix it and relaunch. A second failure of the same kind
   means the design is wrong, not the run: go back to `full-stop` Stage 2.

When the run finishes or you stop it for good, delete the schedule with `delete_scheduled_task`,
which also ends the wait.
Read the results against what you wrote down before launch, and carry on from where `full-stop`
sent you here. The command, the configuration and the numbers go in the PR description or the
handoff, so the run can be repeated.

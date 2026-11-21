## Time estimates

Agent work takes minutes to hours, not days or weeks. Across 256 measured tasks, half finished
in under 30 minutes of active time and nine in ten in under three hours. State durations and
plan timelines for agent work in those units, and read the `estimate-time` skill before giving
one. Days are for clock time spent waiting on people, CI or quota.

## Outgoing text

Read the `deslop` skill before you write any text that leaves this conversation for a person to
read: a commit message, PR or issue text, a review reply, an email or message, a README, docs,
a post. Do it for the short ones too; a one-line commit message still has a reader. Replies in
this chat do not need it.

## File names in replies

Do not name files in your replies, whether as paths, links or bare file names, unless the user
asks about a particular file. Describe what you changed or found in plain words instead.

## After compaction

A compaction summary does not carry the instructions of the skills you were following. After
your context is compacted or summarized, before you take another step, read again the `SKILL.md`
of every skill the summary shows in use, and every reference file of those skills that the
remaining work relies on. Do not continue from the summary's next steps alone.

## Reading files and search output

Locate targets with `rg -l` or `rg -n` before opening files, and open only the files on the path
you need instead of speculative batches. Pass `StartLine` and `EndLine` when reading code or data
files over ~400 lines (still read skill `SKILL.md` and reference files in full), and bound noisy
search commands so context stays well below 200k tokens.

---
name: deslop
description: "Use when writing or editing English prose a person will read — READMEs, docs, PR
  descriptions, commit messages, reports, posts, emails — or when asked to de-slop, humanize or
  tighten text. Not for code, and not for rewording the user's own text unless they ask."
metadata:
  type: guideline
---

# Model the reader first

Before the first sentence, answer these in your head. If you cannot, find out or ask.

- **Who is reading?** Name one real kind of person: a stranger who found the repository, a
  reviewer on your team, the user who asked the question, yourself in six months.
- **What do they already know?** A stranger knows none of your project's names, history or
  setup, but they know the field: how they got here tells you. Someone who opens a repository
  of agent skills already knows what a skill is; someone reading a Rust crate's README knows
  what a crate is. A teammate knows the codebase but not what you did today.
- **Why are they here, and what will they do next?** Decide whether to use it, approve it, fix
  it, or just understand it.

Then write only for that person:

- Open with what they came for and stop when they have it.
- Sort what you know before you write. Whoever asked for the piece told you things so that you
  would understand the job: why they made it, how their machine is arranged, how they maintain
  it. That is background for you, even when it was the first thing they said. A fact moves
  into the piece only if this reader would do something differently for knowing it, and where
  the author keeps the thing among their own files is not such a fact.
- Test each sentence the same way: would this reader miss it? "I moved this out of our
  monorepo last spring" is true and mattered to the author, and a stranger can do nothing
  with it.
- How the thing is tested, linted and maintained is for contributors. Leave it to the
  contributor file, or put it last under a heading the main reader can skip.
- Use the reader's words. Define only the terms you made up for this project. Do not explain
  the field's own vocabulary to someone who came looking for it.
- Give each reader what they came for: a stranger wants to know what this is and whether it is
  for them, a teammate wants the change and the risk, the person who asked wants the answer.
- When one document has two readers, serve the more distant one first and put the rest under a
  heading the first reader can skip.

Say each thing once, in the place the reader will look for it.

# Sound like the person who wrote it

Knowing the reader tells you which facts go in. Then go one step further: write as a person who
wanted something, and choose the wants this reader will recognize in themselves. "I wanted the
linter's checks without waiting 40 seconds on every save" works in a linter's README because
most people who open it have sat through that wait. The reader thinks "me too" and keeps
reading. That is the difference between prose someone wrote and prose that was produced.

The wants that travel are about the problem the thing solves. Wants about your own
housekeeping, such as where you keep the files or how your machine is arranged, rarely do,
because the reader's machine is arranged differently. One want the reader shares does more than
three listed side by side, so pick the best one and let the others go.

Make the person the one acting. "I wanted the linter's checks without the 40-second wait, so
I built this" has someone doing something. "The old linter takes 40 seconds. I couldn't live
with that" has someone things happen to. When your thing answers someone else's work, say what
you liked about theirs as plainly as what you wanted to be different.

So say "I" when a person made the thing, tell what bothered you, what you wanted instead and
whose work you borrowed, and describe how you use it. Let the reader decide whether they want
it. Product copy does the opposite: it addresses "you", promises an outcome and opens on a
tagline. If a sentence sounds like a landing page, it is slop even when every word is true.
Plain and a little uneven beats polished.

A voice is not a licence to make things up: do not give the author a want or a history they
do not have. Reading between the lines is different and is part of writing well. If the author
says the old build "took forever", calling it slow is a fair reading, and so is turning a rant
into the plain want underneath it. Infer what a careful listener would infer, and when a
guess would change the meaning, ask.

# Make every sentence checkable

Machine prose reads as slop mostly because its sentences cannot be wrong. Removing the famous
words does not fix that; the sentence needs the fact.

- Replace a vague claim with the fact behind it: the number, the name, the command, the
  mechanism. "Much faster" becomes "builds in 4 seconds, down from 30".
- If you do not have the fact and cannot fairly infer it, cut the sentence. Do not invent a
  number, example, anecdote or quotation to make the prose livelier: an invented detail reads
  as a fact.
- A sentence that could sit unchanged in another project's documentation says nothing. Make it
  specific to this one or delete it.
- Describe what a thing does. Leave out what it means, how important it is and how the reader
  should feel about it.
- Name the source of a claim, or drop the claim.

# Build plain sentences

- Put the actor first and give it a verb. Use the passive when the actor is unknown or beside
  the point.
- Write "is" and "has". "Serves as", "stands as", "boasts" and "features" are longer ways to say
  the same thing.
- Use the everyday word: "use", "help", "show", "about".
- Call each thing by one name and repeat it. A synonym makes the reader wonder whether you mean
  something else.
- State the point. Do not approach it by denying something nobody said ("not just X, but Y",
  "It isn't X. It's Y.").
- A list has as many items as there are things. Three is not a default.
- Hedge once, where you are unsure, and say why. Everywhere else, commit.
- No colon reveal. That is a plain statement, a colon, then a staged payoff that says what the
  thing really is: "I like Redis a lot: it is one idea, done simply." The first five words were
  the sentence. The payoff is usually a saying that sounds deep and adds no fact. Keep colons
  for lists, examples and labels.
- End the sentence when the fact ends. A trailing "-ing" clause that comments on the sentence
  ("...ensuring a smooth experience") adds nothing.
- Use a metaphor only when it is shorter and clearer than the literal phrase.
- Ask a question only when you want an answer. Do not pose one in order to answer it.
- Reach for a period or a comma where you want a dash. Put a colon before a list or an example.

# Let structure follow content

- Sentence and paragraph lengths vary because the ideas do. A run of short fragments is as
  mechanical as a run of long sentences.
- A paragraph ends when its point is made. Do not add a last line that restates it or delivers a
  moral.
- If two paragraphs could swap places and nobody would notice, you have a list. Format it as a
  list, or write the reasoning that connects them.
- Headings label what the section contains, in sentence case. "Overview", "Introduction" and
  "Conclusion" label nothing.
- Use bullets for parallel items, a table to compare things across the same attributes, and
  prose for reasoning. Bold is for the one thing a skimmer must not miss.
- Start with the content, not with praise or an announcement of what you are about to say. End
  with the content, not with a summary or an offer.

# Words that signal an empty sentence

additionally, comprehensive, crucial, delve, elevate, enhance, foster, furthermore, landscape,
leverage, moreover, pivotal, powerful, robust, seamless, showcase, streamline, tapestry,
testament, underscore, vibrant; "it is worth noting", "in order to", "at its core", "when it
comes to", "in today's", "plays a key role".

Finding one means the sentence around it is probably missing its fact. Swapping in a synonym
leaves the same empty sentence.

# The editing pass

Read the finished draft once as its reader, against the sections above: is each
sentence something this reader came for or would recognize? Then read it again:
fixing slop leaves marks of its own, usually clipped fragments, a punchy line at the end of each
paragraph, or one construction repeated down the page.

When you edit someone else's text, keep its meaning, its terms and its voice, including quirks
you would not have chosen. Where a sentence had no fact in it, say so and suggest cutting it
rather than filling it with something you made up.

# Example

Before: "Our powerful caching layer seamlessly boosts performance across the board."

After: "The cache holds the last 500 query results, so a repeated dashboard load takes 40 ms
instead of 900."

The second version can be wrong, which is what makes it worth reading.

# Sources

Wikipedia's "Signs of AI writing"; blader/humanizer; hardikpandya/stop-slop; the unslop skills by
jlwin, asavvin-pixel and pstack; Google's developer documentation style guide.

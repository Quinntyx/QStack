---
name: deslop
description: "Use when writing or editing English prose a person will read — READMEs, docs, PR
  descriptions, commit messages, reports, posts, emails — or when asked to de-slop, humanize or
  tighten text. Not for code, and not for rewording the user's own text unless they ask."
metadata:
  type: guideline
---

# Know the reader

- Decide who reads this and what they will do next. Open with what that reader needs most, and
  stop when they have it.
- Say each thing once, in the place the reader will look for it.
- Write the draft from the facts, not from a template. If you do not know what the piece is
  claiming, find out before you write a sentence of it.

# Make every sentence checkable

Machine prose reads as slop mostly because its sentences cannot be wrong. Removing the famous
words does not fix that; the sentence needs the fact.

- Replace a vague claim with the fact behind it: the number, the name, the command, the
  mechanism. "Much faster" becomes "builds in 4 seconds, down from 30".
- If you do not have the fact, cut the sentence. Never invent a number, example, anecdote or
  quotation to make the prose livelier: an invented detail reads as a fact.
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

Read the finished draft once as its reader, against the sections above. Then read it again:
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

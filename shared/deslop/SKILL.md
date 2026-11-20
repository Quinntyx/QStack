---
name: deslop
description: "Use before writing any English text that leaves the conversation for a person to
  read, however short: commit messages, PR and issue text, review replies and comments, emails
  and direct messages, READMEs, docs, posts, reports saved to a file. Also when asked to
  de-slop, humanize or tighten text. Not for replies in the chat itself, not for code, and not
  for rewording the user's own text unless they ask."
metadata:
  type: guideline
---

# Model the reader first

Before the first sentence, answer these in your head. If you cannot, find out or ask.

- **Who is reading?** Name one real kind of person, or the one person: a stranger who found
  the repository, a reviewer on your team, whoever reads this commit in the log next year, the
  colleague the email is addressed to.
- **What do they already know?** A stranger knows none of your project's names, history or
  setup, but they know the field: how they got here tells you. Someone who opens a repository
  of agent skills already knows what a skill is; someone reading a Rust crate's README knows
  what a crate is. A teammate knows the codebase but not what you did today. Someone you are
  replying to knows everything already said in the thread, so read all of it first and leave
  out what they said and what was settled.
- **Why are they here, and what will they do next?** Decide whether to use it, approve it, fix
  it, answer it, or just understand it.

Then write only for that person:

- Open with what they came for and stop when they have it. In a reply that is the answer, and
  each question they asked gets one. When you write first, it is what you want from them. A
  refusal goes first too, with its real reason given once and the alternative if there is one.
- Make an ask answerable in a line: what you need and, when the author has a date, by when.
  "Could you send the March invoice by Friday?" can be answered. "Let me know your thoughts"
  cannot.
- Put in what they need to act without writing back: the day and the time, the file, the link,
  the number.
- A reader who does not know the author needs one sentence saying who is writing and why to
  them, before the ask.
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

# Model the speaker and the relationship

Knowing the reader tells you which facts go in. It does not settle how the piece sounds, and a
model left to itself writes everything in the same even, polite voice with no feeling in it.
That voice suits a calm author, in a commit message or a reference page. Anywhere else it
loses what makes a reader act. A complaint written in it can be left for another week, a
thank-you reads as a receipt, and a README has nobody in it for the reader to recognize.

Work the voice out in five steps before the first sentence. They come from research on how
people ask, press and thank each other, listed under Sources. For a commit message the five
take a moment. For a message to someone the speaker needs something from, they are most of
the work.

## 1. Name what the piece does

A piece of writing acts on its reader, and each kind of act is the speaker's to perform only
when something is true of the speaker.

| The piece | For example | It holds only if the speaker |
| --- | --- | --- |
| tells | a claim, a report, an explanation | knows it or has grounds for it |
| asks | a request, an instruction, a deadline | may ask this much of this reader |
| commits | a promise, an offer, a warning of what comes next | has decided to do it and can |
| expresses | thanks, an apology, a complaint | feels it |
| decides | an approval, a refusal, a resignation | holds the role that decides |

Most pieces do several of these. Name the main one, because the others serve it.

When you write for someone else, you cannot make any of these conditions true. They come from
what the speaker told you, from the material, or from what a careful listener would infer: if
the speaker says the old build "took forever", calling it slow is fair. An act whose condition
you cannot find stays out of the piece. That rules out a date the speaker did not set, a
warning they did not give, an apology they did not offer, a feeling they do not have, and a
claim about the reader's side that they cannot know, such as how the reader's system works or
why something went wrong there.

## 2. Measure where the two stand

Five things decide how the act will land.

- **Distance.** How well do the two know each other?
- **Power.** Who can do what for or to whom? Look at where it comes from: a right or a role,
  the means to reward the other or to cost them something, expertise, being liked or trusted,
  holding the evidence. Then ask what happens to each of them if the reader does nothing. The
  one who loses more from silence has less power.
- **Cost.** What does the act take from the reader? Count time, effort, money and risk. Count
  face as well: being told they were slow or wrong costs a reader something.
- **Future.** How long will the two go on dealing with each other, and does the speaker want
  that to continue? A tenant and a landlord have the rest of the lease ahead of them. A
  customer closing an account has nothing ahead and wants nothing.
- **Memory.** Who will read this, and will they remember the speaker? A named person who
  answers their own mail remembers. They have some say in how much trouble to take, and they
  take more for people who were easy to deal with. A support queue is answered by whoever is
  on shift, following a policy, and the speaker's manner does not follow them to the next
  ticket.

Measure these for this act between these two people. The same contributor writes to the same
maintainer with more weight when asking for a review this week than when asking which branch
to target.

## 3. Derive the approach

Start from the reader's last move, because a relationship that continues is a series of turns.
In studies of repeated dealings the approach that does best is a plain one: open by
cooperating, answer what the other side just did in kind, forgive as soon as they cooperate
again, and be easy to read. So a reader who tried to help gets cooperation back, even when the
help did not work. A reader who refused gets a firm answer, and nothing beyond what they did.

Forgiving means the account is closed. Once the reader has done what the speaker wanted, the
piece does not go back to their earlier miss or to the pressure the speaker used to get there.
The cost the speaker named while asking was a lever, and a lever repeated after the reader has
moved is a reproach. A thank-you that recalls what the speaker nearly lost because of the
reader thanks them and blames them in one sentence. Thanks are about what the reader did.

Then weigh the act. It weighs more the more distant the reader is, the more power the reader
holds over the speaker, and the more it costs the reader. Say a light act straight. As the
weight rises, the piece does more for the two things a reader wants from anyone who writes to
them, which are to be thought well of and not to be pushed. It acknowledges what the reader
has done, gives the reason for the ask, makes the ask small and easy to grant, and leaves them
room to decide.

Then set this one result against the future. Future and memory together say what the
speaker's manner today is worth later. When the two have years ahead and the reader will
remember, the relationship is worth more than this result, and the piece gives ground however
strongly the speaker feels: it asks for less than the speaker could, lets a slight pass, and
leaves the reader glad to hear from them next time. When the speaker wants no future with the
reader, manner buys nothing, and the piece is as direct as the speaker's power supports. When
there is a future but nobody on the other side will remember, only this exchange counts: be
civil to the person on shift and as firm as the power supports.

What moves the reader depends on who they are. A person with a say is moved by wanting to help
someone who has been decent to them. A role following a policy is moved by what the policy
recognizes: a right, a rule, a higher level the case can go to, a cost to the organization.
The speaker can press only with what they hold, so find which of these they have.

| The speaker holds | The piece presses by |
| --- | --- |
| a right or an agreement | naming it and what is owed under it |
| evidence | showing it again |
| something the reader said they would do | reminding them of it |
| an alternative they have decided to take | saying what they will do |
| the reader's goodwill and nothing else | keeping it: patience, the stakes, one small ask |

Pressure the speaker cannot back reads as a bluff or as rudeness.

Use the least pressure that could work at this point in the exchange. Pressure has an order.
The first time the speaker asks after something late, the piece is a plain question. After a
plain question that got no answer or a vague one, it recalls what the reader said they would
do. The stakes come after that, and the alternative comes last. Where this piece sits on that
ladder comes from the thread: count what the speaker has already said and what came back. A
reader who answers the plain question never needed pressing, and every step used early is one
the speaker cannot use later.

The speaker's feeling takes the same route. How strongly they feel tells you how much the
piece has to carry, and the steps above tell you in what form. Two angry people write
different messages. One is leaving a company and holds a right, so the piece insists. The
other needs the same office for years and holds only evidence, so the anger arrives as thanks
for what was tried, the evidence once more, what is at stake, and patience. What the speaker
told you about their mood is for you. A piece can carry a feeling without stating it.

## 4. Fit the medium

Every medium has a form its readers expect. A piece that ignores it reads as written by
someone who does not belong there: an email pasted into a chat, or a chat line sent as an
email. Three questions give the form.

- **Can the reader answer at once?** In chat they can, so a message is one turn in an
  exchange and not the whole case. The piece is that one turn: the least that lets the reader
  answer. Between people who talk every day that is often one question with no greeting, no
  background and no reason: "@Dana design doc reviewed yet?" She knows what she said she would
  do and when, and the question alone tells her someone is waiting. Why the speaker needs it,
  how long it has been and what it is holding up belong to a later turn, if her answer calls
  for them. Put in the first turn, they make a quick question read as a prepared statement. In
  email, on a ticket or in a form, each round takes
  hours or days and a gap costs a day, so one message has to be complete: everything the
  reader needs to act is in it.
- **Who else reads it, and how long is it kept?** A direct message is for one person today. A
  commit message, an issue or a ticket reply is for strangers months from now, who find it by
  search, so it names things in full.
- **What does a message between these two normally look like here?** Look at the thread or at
  the speaker's earlier messages for the greeting, the length, the sign-off and the
  formatting, and keep that form. A two-line question gets a few lines back. With nothing to
  look at, use the medium's usual form.

| Medium | Usual form |
| --- | --- |
| Email | A subject that names the matter and what is wanted. A greeting by name, as formal as the distance between the two. Plain paragraphs, since markup shows as typed. One line of thanks when something is asked. A sign-off and the speaker's name. |
| Chat or direct message | No subject, no sign-off, and no greeting beyond a mention of the name. One point, in about the words the two would use across a desk. What both already know is left out. More distance or a first contact earns a line of who is asking and why. A second point is a second message. |
| Support form or ticket | No greeting needed. The account or order number first, then what happened, then what is wanted. |
| Commit, pull request, issue | The repository's own convention for titles and sections. What changed and why, in full names a stranger can search for. |

The courtesies a medium expects are part of its form. An email without a greeting, a thank-you
for the favour asked or a sign-off reads as curt whatever the sentences between them say, and
a chat message with all three reads as stiff.

## 5. Check the four sides

A reader takes four things from any piece, whether or not the writer put them there.

- **The matter:** the facts.
- **The speaker:** what the piece shows of the person behind it, what they want and how they
  feel.
- **The relationship:** how the speaker sees the reader, as a helper, a peer, an obstacle or a
  subordinate. The tone and the form of the ask carry this. No sentence states it.
- **The appeal:** what the speaker wants the reader to do.

Flat text fills in the matter and leaves the other three to chance. Decide all four, then read
the draft once for each. A wrong approach shows on the relationship side. A deadline set for
someone who owes the speaker nothing tells them the speaker thinks they work for the speaker.

Tone travels badly in writing. In experiments, people writing email were much more confident
that their tone would come through than their readers' guesses justified. Readers also tend to
take a message as cooler or more hostile than it was meant. So write warmth out in words, a
little more than feels needed, and write displeasure as facts, a little cooler than the
speaker feels it.

## Three cases

A customer's refund is five weeks late. The piece asks for what is owed. The seller's last
move was silence. The two will not deal again, and the message goes to a support queue where
nobody will remember it. The speaker holds the seller's own refund policy and has decided to
dispute the charge. Granting the ask costs the seller nothing it does not owe. The act is
light, the power is real and there is no future to protect, so the piece says it straight: the
policy, the days, the refund wanted and the dispute that follows.

A contributor's pull request has had no review for three weeks. The piece asks a favour: an
hour of a maintainer's time. The maintainer is one named person who will remember, decides
whether the patch is ever read, owes the contributor nothing, and will see the contributor's
name on every later patch. The contributor holds the patch and its passing tests and nothing
else. The ask implies the maintainer has been slow. The act is heavy and the future is long,
so the piece gives ground. It says what the patch fixes and for whom, shows that it is ready
to read, asks for one thing and leaves room to answer. The contributor may be fuming. The
maintainer reads a person they would be glad to hear from again.

A developer publishes a tool. The README offers it. The reader has never heard of the author,
can close the tab, and risks an afternoon by trying it. The author holds only what the tool
does. So the piece opens on a want the reader shares, shows what the tool does with numbers,
says how to try it and leaves the choice with the reader.

## Presenting something to strangers

The third case covers a README, a post or an announcement, and it has its own habits. Write as
a person who wanted something, and choose the want this reader will recognize in themselves.
"I wanted the linter's checks without waiting 40 seconds on every save" works in a linter's
README because most people who open it have sat through that wait. The reader thinks "me too"
and keeps reading. The wants that travel are about the problem the thing solves. Wants about
your own housekeeping, such as where you keep the files or how your machine is arranged,
rarely do, because the reader's machine is arranged differently. One want the reader shares
does more than three listed side by side, so pick the best one and let the others go.

Make the person the one acting. "I wanted the linter's checks without the 40-second wait, so
I built this" has someone doing something. "The old linter takes 40 seconds. I couldn't live
with that" has someone things happen to. When your thing answers someone else's work, say what
you liked about theirs as plainly as what you wanted to be different. So say "I" when a person
made the thing, tell what bothered you, what you wanted instead and whose work you borrowed,
and describe how you use it. Product copy does the opposite: it addresses "you", promises an
outcome and opens on a tagline. Those are acts of a speaker with authority over the reader,
and this speaker has none. If a sentence sounds like a landing page, it is slop even when
every word is true. Plain and a little uneven beats polished.

## Writing under someone else's name

Take the details of the relationship from the speaker. Their earlier messages show what they
call this person, how they sign and how formal the two of them are. Keep those, so the piece
still reads as coming from them. Then write it better than they would have. Better means more
likely to get them what they want from this reader, which is not the same as more polished or
more polite. Advice you give beside the draft serves the speaker's aim as well, so do not
suggest they do the thing the piece refuses to do.

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
- End the sentence when the fact ends. A trailing "-ing" clause that comments on the sentence
  ("...ensuring a smooth experience") adds nothing.
- Use a metaphor only when it is shorter and clearer than the literal phrase.
- Ask a question only when you want an answer. Do not pose one in order to answer it.
- Reach for a period or a comma where you want a dash. Put a colon before a list or an example.

# Patterns with names

Each of these stages a point instead of making it. The fix is the same every time: write the
plain claim, or cut the sentence if there is none.

- **Colon reveal.** A statement, a colon, then a payoff that says what the thing really is: "I
  like Redis a lot: it is one idea, done simply." The first five words were the sentence. Keep
  colons for lists, examples and labels.
- **Saying that sounds deep.** "Symmetry is the language of trust." "X is the Y of Z." An
  ordinary point dressed as an aphorism, anywhere in the text and not only at a paragraph's end.
- **Balanced pair.** A phrase polished to mirror the one before it: "the same thing for how I
  work, at a price I can pay."
- **Staged run-up.** "Here's the thing", "Let's dive in", "Honestly", "The real question is",
  "What most people miss". These announce candor or insight before a routine claim. Inserted
  folksiness is not a voice.
- **Stock opener and closer.** "I hope this finds you well", "I wanted to reach out", "Just
  circling back", "Thank you for your patience", "Please don't hesitate to reach out", "Let me
  know if you have any questions". They are stock when the sender does not mean them, and then
  the message loses nothing without them. A thank-you or a good wish the sender does mean is
  content, and the greeting and sign-off a medium expects are part of its form.
- **Echo.** The reader's own message handed back before the answer: "Thanks for your question
  about the latency numbers." They know what they asked.
- **False agency.** A thing gets a human verb so nobody has to be named: "the data tells us",
  "the decision emerged", "a complaint becomes a fix". Say who did it.
- **Phantom objection.** "To be clear", "You might think", "This is not to say". The text
  answers a claim nobody made.
- **Weightless concession.** "Despite these challenges, X continues to", or two sides set out
  with no verdict. Say which side you take.
- **Empty range.** "From startups to enterprises", "from concept to launch". Name the things
  you mean.
- **Intensifiers and extremes.** "Really", "simply", "genuinely", "actually", "always",
  "everyone". They add stress without adding a fact.
- **One source made plural.** One review becomes "reviewers", two posts become "widespread
  coverage".

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

Read the finished draft once as its reader, against the sections above: is each sentence
something this reader came for or would recognize? Read it once more for each of the four
sides, and check that every act in it is one the speaker can perform. Then read it again:
fixing slop leaves marks of its own, usually clipped fragments, a punchy line at the end of
each paragraph, or one construction repeated down the page.

When you edit someone else's text, keep its meaning, its terms and its voice, including quirks
you would not have chosen. Where a sentence had no fact in it, say so and suggest cutting it
rather than filling it with something you made up.

# Examples

Before: "Our powerful caching layer seamlessly boosts performance across the board."

After: "The cache holds the last 500 query results, so a repeated dashboard load takes 40 ms
instead of 900."

The second version can be wrong, which is what makes it worth reading.

Before: "Hi Mr. Castellano, I hope this message finds you well! I wanted to reach out about an
issue with the dishwasher in my unit. Please let me know when you might be able to take a look.
Thank you so much for your time!"

After: "Mr. Castellano, the dishwasher in 4B has leaked from the door since Saturday and there
is water under the cabinet. Could someone look at it this week? I'm home Wednesday and Friday
after 4."

The second version tells him how bad it is and when he can come in, so he can reply with a
time. Every fact in it came from the tenant. Without those facts, ask before you write.

Before: "Hi, I'm just following up on my refund request from last month. I understand you
must be busy! Please let me know if there are any updates. Thanks so much for your help."

After: "I returned the monitor on March 3 and your tracking shows it reached you on March 6.
Your policy says a refund takes 10 business days. It has been 31. Refund the $412 to my card
by Friday. If it has not arrived by then, I will dispute the charge with my bank."

The sender is a customer who is owed money, and the first version hid that, so the reader
could leave it for another week. The second gives the reader a date and a cost for missing it.
The sender had already chosen Friday and decided to dispute the charge. A draft does not add
either one.

Before: "Thanks for the notes. They were helpful."

After: "Thank you for sending your notes from Thursday. I was out sick and expected to spend
the weekend rebuilding the lecture from the slides. With yours I was caught up in an hour. I
owe you a coffee."

The first version is accurate and reads as a receipt. The second tells her what her notes
saved, which is the reason the sender wanted to write at all.

# Sources

For the prose rules: Wikipedia's "Signs of AI writing"; blader/humanizer;
hardikpandya/stop-slop; the unslop skills by jlwin, asavvin-pixel and pstack; Google's
developer documentation style guide.

For the speaker and the relationship:

- John Searle, *Speech Acts* (1969): the kinds of act and the conditions each one needs.
- Penelope Brown and Stephen Levinson, *Politeness* (1987): distance, power and cost, and
  saying more for the reader as the three rise.
- Robert Axelrod, *The Evolution of Cooperation* (1984): repeated dealings, answering in kind,
  and how much the future is worth.
- Michael Lipsky, *Street-Level Bureaucracy* (1980): the say a front-line person has, and whom
  they use it for.
- John French and Bertram Raven, "The Bases of Social Power" (1959), with Raven's 1965
  addition: where power comes from.
- Roger Fisher and William Ury, *Getting to Yes* (1981): what each side is left with if
  nothing is agreed.
- Robert Cialdini, *Influence* (1984): people act to stay consistent with what they said.
- Herbert Clark and Susan Brennan, "Grounding in communication" (1991), and JoAnne Yates and
  Wanda Orlikowski, "Genres of organizational communication" (1992): what a medium lets its
  users do, and the forms readers come to expect in it.
- Friedemann Schulz von Thun, *Miteinander reden* (1981): the four sides of a message.
- Justin Kruger and others, "Egocentrism over e-mail" (2005), and Kristin Byron, "Carrying
  too heavy a load?" (2008): how tone is misread in email.

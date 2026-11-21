---
name: model-selection
description: "Use when choosing which model, effort and provider a child agent runs on, or when a
  skill points here for the builder model."
metadata:
  type: guideline
---

# Who does what

Edit these in plain words.

- **The thread's own model** does everything that needs judgment: research, design, reading the
  code that comes back, diagnosing bugs, cleanup, small or tightly coupled edits, and every
  decision. That work stays in the thread unless the user asks to delegate it. Do not delegate work
  when writing a tight brief and checking the diff would cost more than making the edit directly
  (typically a few dozen lines or tightly interwoven edits).
- **Builders** implement cleanly separable chunks of work from an explicit brief. They do not
  research, diagnose, design or review. Two builders are in use and being compared:
  - **DeepSeek V4.1 Flash**, through OpenCode Go on Pi, always at max effort. The baseline
    builder.
  - **Hy4 Flash Free**, on the **OpenCode** provider (`opencode`; it only runs on OpenCode and
    cannot run on Pi), at max effort or its highest available thinking setting. It is currently
    free and being evaluated against DeepSeek V4.1 Flash; keep it on a tighter leash than DeepSeek
    with smaller, more explicit chunks and closer diff inspection.
  - **Mixing and fallbacks:** Mix and alternate between the two so both get comparison data without
    hurting output quality. When a task has two or more cleanly separable chunks, give at least one
    chunk to each; on a single-chunk task, pick with `shuf -n1 -e deepseek hy4`. Give intricate
    chunks to DeepSeek (or handle them in the thread). If the OpenCode provider is disabled or Hy4
    Flash Free is not listed in `orchestrator_capabilities` on this machine, use DeepSeek V4.1
    Flash and note that Hy4 was unavailable. Under quota pressure (OpenCode Go or DeepSeek rate
    limits or quota errors), switch builder work to Hy4 Flash Free while it is free and OpenCode is
    available, and note the switch.
  - **Builder review:** After reading each builder's diff (either model), emit one searchable
    `builder_review:` line in intermediate thread output so thread-history search finds it across
    runs, and include a short 1-2 line overall builder note in your final report:

    ```
    builder_review: <model> | chunk: <brief scope & size/complexity> | adherence: <good/partial/poor> | rework: <none/minor/heavy> | <one-line verdict>
    ```
- **Where failure is expensive, no cheap builder.** When a mistake would burn hours of compute
  or cannot be undone, such as a model training run, a long benchmark or a migration over real
  data, a weak implementer can waste far more than it saves. The thread's own model does that
  step directly. A builder may still write what leads up to it.
- **Council seats** are listed in the Panels section of `../../council/SKILL.md`, with their
  efforts.
- A model the user names for a task is used exactly as named, for that task.

# Routing

- With `delegate_task`, route Claude models to the Claude Code provider, Gemini/Antigravity models
  to the Antigravity provider, Hy4 Flash Free to the **OpenCode** provider (`opencode`; never Pi),
  and other open-weight or GPT Sol/Astra models (including DeepSeek V4.1 Flash via OpenCode Go) to
  Pi (the Pi T3Main provider), even when another provider also lists them.
- Inside a native dynamic workflow in Claude Code, every model that workflow can reach runs inside
  Claude Code, the non-Claude ones included, so the workflow keeps running without a break
  (OpenCode-only models like Hy4 Flash Free are skipped there and fall back to DeepSeek).
- `orchestrator_capabilities` is the live list of what this thread can reach (pass `search` when
  looking up a model outside the short list). Call it once per thread, and again only after an
  error or when the user names a different provider. Pass effort or thinking in `target.options`
  using the option name `orchestrator_capabilities` reports for that model, for example
  `{effort: 'max'}` or `{thinking: 'max'}`.

# When a model is not listed

Say which model is missing and stop there, except for the declared fallbacks between DeepSeek V4.1
Flash and Hy4 Flash Free above. Do not pick another substitute, change provider or lower the effort
unasked. The user decides what runs instead.

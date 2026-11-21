---
name: harness-config
description: "Use when a skill names harness-config, or when changing Antigravity's settings,
  rules, skills or MCP configuration, choosing where an Antigravity skill is deployed, or
  bootstrapping repository guidance. Antigravity binding for skill and configuration editing."
metadata:
  type: guideline
---

# Ownership

- Resolve managed configuration to its owner's source before editing. Skills installed from QStack
  are copies with a `.qstack-source` file naming the QStack clone; edit that repository and rerun
  `bin/qstack install antigravity`, never edit the installed copies directly.
- T3 Code owns its downloaded Antigravity ACP runtime and private provider profiles. Use provider
  settings for runtime installation, binary selection and sign-in. Keep credentials, caches and
  generated profile files out of tracked source.
- System Antigravity and T3's managed agent share user skills in `~/.gemini/config/skills/`.
  T3 links that directory into its private `GEMINI_HOME` when preparing a provider session. Install
  user skills at the shared location, not beside the downloaded executable or inside that profile.

# Skill loading

- A skill lives at `<name>/SKILL.md`, directly inside a skills root. Global skills use
  `~/.gemini/config/skills/`; project skills use `.agents/skills/`. The CLI also reads
  `~/.gemini/antigravity-cli/skills/`; T3 supports that user root too.
- Keep nested children on explicit relative routes from their parent skill. A nested `SKILL.md`
  does not become an independently advertised skill.
- Check discovery in a new session on the intended surface. In T3, use a new provider session so
  its private profile can pick up a newly created global skills directory.

# Rules and settings

- Global context uses `~/.gemini/GEMINI.md`; repository context uses `AGENTS.md` or `GEMINI.md`.
  QStack adds only its marked block to the global file and leaves other text intact.
- Read the current Antigravity settings schema before changing configuration. Claude invocation
  controls and Pi profile settings are not Antigravity settings.
- For repository guidance, use agent-repo-guidance and the existing repository instructions.
  There is no assumed native guidance bootstrap.

# References

Paths checked against Google's [customization discovery documentation](https://antigravity.google/docs/customization-discovery/)
and T3 Code's [Antigravity guide](https://github.com/pingdotgg/t3code/blob/main/docs/user/providers-antigravity.md)
on 2026-11-19. Recheck those sources when loader behavior changes.

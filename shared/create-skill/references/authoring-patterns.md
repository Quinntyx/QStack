# Authoring patterns and research basis

Read this when choosing a router, shared reference, or example. This reference inherits the
create-skill contract; it does not grant tool or publication authority.

## Choose the context boundary

- Inline what every branch needs. Put branch-specific detail behind a pointer that names both its
  subject and the condition for reading it. A vague optional-looking pointer to a required contract
  creates unreliable execution; fix the pointer instead of duplicating the contract.
- Keep a recipe's steps visible and reference detail nearby or disclosed. Choose a separate advertised
  skill only when it has a useful independent trigger; each advertised description spends context.
- Parent routers own selection and shared invariants. Children own the selected operation. References
  supply detail under that contract. This is intentionally different from requiring standalone leaves.
- Read the target loader before choosing invocation controls; the `harness-config` skill records
  each harness's controls and discovery rules. Keep children on explicit parent routes.

## Useful examples

An output-format example earns its space when a description leaves real ambiguity:

```text
Input: draft a reply to review comment 17, without posting
Output: unpublished reply text, intended repository/thread, and supporting check
Effect: no hosted comment, issue, or PR mutation
```

The rule is publication scope, not the incidental number 17. Pair this with a published-response
case only if that contrast is otherwise unclear. For syntax examples, verify the installed command's
help or tool schema and show placeholders that cannot be mistaken for real credentials.

Examples are unnecessary for a familiar rule that already has a clear measurable result. Move a
catalog of examples out of the entrypoint; retain only those needed for the current branch.

## Sources checked 2026-10-27

- Anthropic skill creator: progressive disclosure and short concrete format examples. Its
  multi-agent benchmark workflow is not used here.
  https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/skill-creator/SKILL.md
- Matt Pocock writing-for-agents: conditional context pointers, separate context/cognitive loads,
  steps versus reference, co-location, checkable completion criteria, and one authoritative owner.
  https://github.com/mattpocock/skills/blob/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/productivity/writing-for-agents/SKILL.md
- Matt Pocock skill mechanics: intentional invocation and router boundaries; translate ideas rather
  than copying unsupported fields across harnesses.
  https://github.com/mattpocock/skills/blob/59db609eb1e18aaf59b63284d0e52255aff0c63c/skills/productivity/writing-for-agents/SKILL-MECHANICS.md
- T3 Code's repository skills: `test-t3-app` is a small task-shaped entrypoint with conditional fixture
  detail and an honest unavailable-tool outcome. `contribution-triage` separates trusted policy,
  dry-run/enforcement authority, current evidence, and read-back before uncertain-write retries.
  Source revision: https://github.com/Quinntyx/t3code/tree/40f3a3c4170d691423189d88245b87bb8040279c/.agents/skills
  Source policies are examples, not authority to transplant T3-specific browser permissions or
  moderation rules into other repositories.

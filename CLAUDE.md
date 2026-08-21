# Working agreements

## Skills

The skills in `~/.claude/skills` encode how I want work done. They are not
reference material to read afterwards — consult them *before* acting.

**Before the first substantive action of a task, check whether a skill covers
it, and invoke it with the Skill tool.** When several apply, invoke the most
specific. When a skill gates work (`brainstorming`, `writing-plans`,
`verification-before-completion`), it runs *before* that work, never as a
retrospective write-up.

This applies to real engineering tasks — building, debugging, reviewing,
shipping. It does not apply to conversational replies, quick lookups, or
answering a question about existing code.

### Routing

| Situation | Skill |
|---|---|
| New feature, component, or behaviour change — before any code | `brainstorming` |
| Pressure-testing an idea before committing to build it | `roast` |
| Multi-step task with a spec or requirements | `writing-plans` |
| Executing a plan that is already written | `executing-plans` |
| Implementing a feature or bugfix | `test-driven-development` |
| A bug, test failure, or anything behaving unexpectedly | `systematic-debugging` |
| Writing, reviewing, or refactoring code generally | `karpathy-guidelines` |
| Reviewing a PR or a set of changes | `code-review-skill` |
| Wanting my work reviewed before it lands | `requesting-code-review` |
| Acting on review feedback I have been given | `receiving-code-review` |
| Auth, user input, secrets, API endpoints, payments | `security-review-checklist` |
| About to claim something is done, fixed, or passing — and before any commit or PR | `verification-before-completion` |
| Work is complete and needs merging, a PR, or cleanup | `finishing-a-development-branch` |
| Frontend or UI design, critique, or polish | `impeccable` |
| Isolating feature work from the current workspace | `using-git-worktrees` |
| Two or more genuinely independent tasks | `dispatching-parallel-agents` |
| Creating or editing a skill | `writing-skills` |

`using-superpowers` is the discovery entry point for the `obra/superpowers` set
— invoke it when a task looks like it should have a skill but the table above
does not name one.

### Notes

- Skill descriptions alone have not reliably triggered activation; this table is
  the mechanism, so prefer it over waiting for a description to match.
- Skills are symlinks into `~/Documents/Claude/claude-skills`, which is the
  single source of truth across all my devices. Edit skills there, never in
  `~/.claude/skills`. See that repo's `SETUP.md`.
- In a Claude Code **cloud** session the symlinks point at
  `~/.claude/claude-skills` instead — a read-only clone of the public mirror,
  refreshed each session by a SessionStart hook. Edits made there are wiped on
  the next session; change skills in the private repo and run `skillctl publish`.
- If a skill's guidance conflicts with an instruction I have given directly in
  conversation, my instruction wins — tell me about the conflict rather than
  silently picking one.

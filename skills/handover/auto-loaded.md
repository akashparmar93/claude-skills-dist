# Handover into an auto-loaded file

Read this when the file the handover goes into is `CLAUDE.md`,
`CLAUDE.local.md`, `.claude/CLAUDE.md` or `AGENTS.md`. Everything in
`SKILL.md` still applies; this adds where the full entry goes and what stays
in the auto-loaded file.

**If the file you would write into is loaded automatically** — `CLAUDE.md`,
`CLAUDE.local.md`, `.claude/CLAUDE.md`, `AGENTS.md` — every byte of it is
re-sent on every turn. The full entry goes in the project's log
(`PROGRESS.md`, `OPEN.md`, a log under `docs/`; if there is none, create
`docs/handover-log.md` without asking), and the handover block holds a
short view of **only the latest entry**:

1. Write the full entry into the log, in the log's own order.
2. Clear the block's older entries. One whose full version the log already
   has is dropped. Every other one moves to the log verbatim, in the log's
   own order (a new log keeps the order they had).
3. Write the short view into the block: every slot as in the full entry,
   except these:
   - **Verified** is shorter than the log's: the machine, the date and
     time, then `` at `<sha>` ``, the test run's result
     (`make test` -> `Ran 31 tests ... OK`), what is broken or not
     verified, and a pointer to the log entry, which keeps every other
     command's result.
   - **Landed, and why** is one line per change or decision, naming where
     its reasons are written — the log entry, a commit, a spec or plan
     section.
   - **Start here**, when the block is more than five lines: the whole block
     goes in the project's Start here file, replacing what it held —
     `docs/start-here.md` unless the project keeps one elsewhere; create it
     without asking. The slot is one line naming that file and its tiers.
4. If the file has other status sections — a `## Next`, a task list, a
   phase summary — rewrite each to the current position and pointers: the
   phase and task now, then where the rest is written (the plan, the
   ledger, the log). History in them (finished tasks, their dates and
   rulings) moves to the log verbatim first, as in step 2. Open items in them
   are a file-level pending list (`SKILL.md` §3): each stays, or moves to the
   log verbatim; a pointer never stands in for an open item.

Do it in the same commit, and say in your closing message how many entries
moved and the file's size before and after.

**If the project's own instructions say to keep every entry in that file**
(for example "add a new entry above the previous ones"), do not pick a
side silently. Follow the rule above, and say in the closing message that
it overrode the project's instruction, quoting it, so the owner can change
one or the other. An instruction only to record the handover there, such as
"record the handover under 'Current status'", is not a conflict: replacing
the block still records it there.

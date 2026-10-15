---
name: handover
description: Use when a working session is ending and the next one will start cold — "let's stop here", "wrap up for today", "hand over", "I'm stopping now" — or before closing any session whose context exists only in the conversation.
---

# Handover

## Overview

The next session inherits the repository. It does not inherit this conversation.

Every fact that currently lives only in chat — why you chose this over that,
what you tried and abandoned, what looks finished but is not — is gone at the
end of this turn unless you write it into the repo.

**A handover is not a summary of what you did. It is what the next session
needs in order to not waste its first hour.**

## 1. Stop at the next clean point

The *next* one. Not a better one slightly further on.

Finish in-flight work only when both are true:

- a test for it is already written and currently failing, and
- getting that test green changes the implementation only — no note, comment,
  or open question anywhere in the repo records the approach as undecided.

If something written down says the choice is open, it *is* open, however
obvious the answer looks to you now. "It's only one more line" is how a stop
becomes another hour.

Otherwise park it, in this order:

1. **Commit it to `main` with the unfinished test skipped**, the skip reason
   naming the handover entry — `@pytest.mark.skip(reason="descending sort
   unfinished — see PROGRESS.md 2026-09-06")` or the project's equivalent.
   `main` stays green and the work stays in the tree, one line from resuming.
2. Only if the project has no skip mechanism, revert it and quote the reverted
   diff in the entry.

Never park work by leaving it on a branch — step 4 deletes the branch.
Never land a *failing* test on `main`.

## 2. Read once, start the checks, write while they run

**REQUIRED SUB-SKILL:** verification-before-completion.

1. **Read everything in one command:** the machine name, the date and time,
   `git status --short`, `git stash list`, `git branch -a`, `git log
   --oneline` since the previous handover, the previous entry alone (`sed -n
   '/^## <its heading>/,/^## /p' <log>`), and `gh run list --limit 3`. Read
   further only where that output points.
2. **Start the Start here block (§3) in the background**, all of it,
   verbatim, its output to a file: the harness's background run, or `bash
   start-here.sh > start-here.out 2>&1 &`. Its test run is the Verified test
   run: the suite runs once, there.
3. **Write the entry while it runs**, every slot but Status and Verified.
4. **When it has finished, read its output**, run what the block does not
   — lint, build, server checks — and write Status and Verified from what
   they *said*, never "tests pass" from memory. If something is broken, the
   entry says so. A handover that hides a failure costs the next session
   more than the failure does.

**CI is recorded, not waited on.** Read `gh run list` once. A run that is
queued or in progress is recorded as pending, with its run id and commit, in
Verified and in Stops here, and Start here gets `gh run list --commit <sha>`
so the next session reads the result. The same holds for the run your own push
starts in §4.

## 3. Write the entry

Find the file the project already uses — `OPEN.md`, `PROGRESS.md`, a log under
`docs/` — and match its ordering and headings; the slots below set each
entry's shape. §2's read gave you the previous entry. Only propose a new
file when there is genuinely none, and ask before creating it.

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
   - **Verified** is shorter than the log's: the machine, the time, the
     test run's result (`make test` -> `Ran 31 tests ... OK`), what is
     broken or not verified, and a pointer to the log entry, which keeps
     every other command's result.
   - **Landed, and why** is one line per change or decision, naming where
     its reasons are written — the log entry, a commit, a spec or plan
     section.
   - **Start here**, when the block is more than five lines: the whole block
     goes in the project's Start here file, replacing what it held —
     `docs/start-here.md` unless the project keeps one elsewhere; create it
     without asking. The slot is one line naming that file, then the two or
     three commands that matter most (machine name, get current, confirm
     green).

Do it in the same commit, and say in your closing message how many entries
moved and the file's size before and after.

**If the project's own instructions say to keep every entry in that file**
(for example "add a new entry above the previous ones"), do not pick a
side silently. Follow the rule above, and say in the closing message that
it overrode the project's instruction, quoting it, so the owner can change
one or the other. An instruction only to record the handover there, such as
"record the handover under 'Current status'", is not a conflict: replacing
the block still records it there.

**Every entry fills these slots. A slot with nothing in it says so. A slot
that has not changed since an earlier entry is one line naming the entry
that holds it in full** — `Start here — unchanged since 2026-10-13 19:45` —
the entry with the text, never one that itself points back. Stops here
keeps its items: a carried one is one line naming the entry with its full
text.

- **Status** — one sentence. What is done and landed; what is not.
- **Verified** — one line, however many commands ran, even where earlier
  entries list them: the machine by name (`scutil --get ComputerName`, or
  `hostname`), the date and time, each command and its headline result, and
  what could not be verified:

  ```
  - **Verified** — Akash’s MacBook Air, 2026-10-15 23:21: `make test` -> `Ran 31 tests ... OK`; `df -h /` (15:02) -> 61% used. Not verified: a restore.
  ```
- **Start here** — the block a cold session pastes first: its first command
  prints the machine name, then get current, get running, confirm green, and
  `gh run list --commit <sha>` for any CI run left pending. It is the block
  §2 ran; "expected output" means output you have actually seen.
- **Landed, and why** — what changed, plus the decisions made this session and
  their reasons. These exist nowhere else.
- **Stops here** — what a cold reader would wrongly assume is finished. Green
  tests over code nothing calls belong here.
- **Next** — the first concrete action. Open questions list their options, so
  the next session does not re-derive them.

**The next session may be on a different machine.** It reads "this Mac", "this
machine" or "here" as its own. So every fact that holds on one machine only —
an env file, a key or token, an installed tool, a linked CLI, a running job —
names that machine: "the CLI is linked to production on Akash's MacBook Air",
not "on this Mac".

## 4. Land it on `main`

Work sitting on a branch is work a cold session will not find. Merge to `main`,
push `main`, delete the branch local and remote. A pushed-but-unmerged branch is
the exact failure this step exists to prevent.

**RELATED:** finishing-a-development-branch, for the merge itself.

## 5. Leave nothing running or dangling

Stop only the services *this* session started — check each pid's working
directory first. Never `pkill` by pattern; you will kill someone else's server.
Remove worktrees you created.

## Closing check — every line must be true

```bash
git status --porcelain          # empty: scratch committed, deleted, or ignored
git stash list                  # empty, or every entry described in the handover
git branch -r                   # nothing stranded — the work is on main
git rev-parse HEAD origin/main  # identical
```

Then tell the user in your reply: what you parked, what you could not verify,
and anything left for them.

## Red flags

| About to... | Instead |
|---|---|
| "It's one more line, I'll just finish it" | Is the test already written? Green without a design decision? If not — park it. |
| Write "all tests pass" | Run them. Record what they said. |
| Run the suite again before committing | The Start here run is the Verified run. Once. |
| Wait for the Start here run before writing | It runs in the background; write the entry meanwhile. |
| Read the log, `git log` and `git status` one by one | One command, §2 step 1. |
| Rewrite a slot nothing changed | One line naming the entry that has it. |
| `gh run watch` until CI finishes | Record the run id as pending; Start here checks it. |
| Leave an untracked scratch file "for them to delete" | Commit it, delete it, or ignore it. A cold session opens a clean tree. |
| Push the branch and stop | Merge to `main`. A branch is not a handover. |
| `pkill -f python` | Find the pid you started. Kill that one. |
| Give next steps as prose only | Prose plus the runnable **Start here** block. |
| Revert unfinished work so `main` stays green | Commit it with the test skipped. Code belongs in the tree, not quoted in a log. |
| "The note says it's open, but the answer is obvious" | Written down as open means open. Park it. |

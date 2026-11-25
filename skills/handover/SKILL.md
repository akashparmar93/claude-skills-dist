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
   '/^## <its heading>/,/^## /p' <log>`), the file's own pending lists outside
   its entries, and `gh run list --limit 3`. Read further only where that
   output points.
2. **Start the Start here block (§3) in the background**: its Every resume
   and Full tiers, verbatim, not On demand, its output to a file: the
   harness's background run, or `bash start-here.sh > start-here.out 2>&1 &`.
   `git rev-parse --short HEAD` as it starts is Verified's `<sha>`. Its test
   run is the Verified test run: the suite runs once, there.
3. **Write the entry while it runs**, every slot but Status and Verified.
4. **When it has finished, read its output whole** — `cat` it, or page it
   by its `===` markers; never through a filter such as `grep -v`: one
   written to drop the progress dots drops result lines too. Run what the
   block does not — lint, build, server checks — and write Status and
   Verified from what they *said*, never "tests pass" from memory. If
   something is broken, the entry says so. A handover that hides a failure
   costs the next session more than the failure does.

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

**If the file you write into is `CLAUDE.md`, `CLAUDE.local.md`,
`.claude/CLAUDE.md` or `AGENTS.md`**, read `auto-loaded.md` in this skill's
directory first and follow it: it says where the full entry goes and what
stays in that file.

**Account for every pending item before you write.** List each item in the
previous entry's Stops here and Next, and each item of any pending list the
file keeps outside its entries (a "Looks finished but is not", a "Next"
section). Then:

- **An item from the previous entry** goes into the new entry as exactly one
  of: **carried**, its own line in Stops here or Next that names the item; or
  **closed**, a line in Landed that names the item and says it is done and
  where. A carried line shorter than the item's full text names the entry or
  file that holds that text, and that place holds it, never another pointer:
  `restore never rehearsed; steps in the 2026-10-10 entry`.
- **A file-level pending list** keeps every item. An item leaves it only when
  it is done, moved verbatim to the project's history. The entry carries one
  line per list: its name and count (`Looks finished but is not — 5 items, 1
  closed this session`).
- **The closing message states the counts:** "N pending items carried, M
  closed", plus each file-level list's count.

**Point, don't retell.** A fact already in a commit message, spec, plan or
project doc gets its location in the entry, not a summary. The commit message
stays a subject and a few lines; it is not where the cut detail goes.


**Every entry fills these slots. A slot with nothing in it says so. A slot
that has not changed since an earlier entry is one line naming the entry
that holds it in full** — `Start here — unchanged since 2026-10-13 19:45` —
the entry with the text, never one that itself points back. Stops here and
Next are never shortened that way: they list every item, one line each.
Every line under Landed, Stops here and Next is at most 250 bytes.

- **Status** — one sentence: what is done and landed; what is not.
- **Verified** — one line, however many commands ran, even where earlier
  entries list them: the machine by name (`scutil --get ComputerName`, or
  `hostname`), the date and time, then `` at `<sha>` `` (at least 7 hex
  characters, `HEAD` when the Start here run began), each command and its
  headline result, and what could not be verified:

  ```
  - **Verified** — Akash’s MacBook Air, 2026-10-15 23:21 EAT, at `4153e97`: `make test` -> `Ran 31 tests ... OK`; `df -h /` (15:02) -> 61% used. Not verified: a restore.
  ```
- **Start here** — the block a cold session pastes first, and the one §2
  ran. It is these headings in this order, each followed by one ```` ```bash ````
  block: `###` in a Start here file, and in a log entry one level below the
  entry's own heading (`#### Full` under `### 2026-10-19 …`):
  1. `Every resume` — prints the machine name, gets current (pull,
     `sync`, a lockfile-gated `npm ci`), then the read-only lines that guard
     against the other Mac differing: toolchain versions, imports, status.
  2. `Full` — the rest: get running, confirm green (suite, lint, build),
     and `gh run list --commit <sha>` for any CI run left pending.
  3. `On demand` — lines that need Akash (`# needs Akash: Touch ID`) or
     have never caught anything. No such lines: no heading.

  A project that keeps a Start here file holds the block there, and a log
  entry's slot is one line naming that file and its tiers. A line already
  under a tier heading keeps its tier; a new or untiered line goes in the
  tier whose description above fits it. Each line's comment is today's
  expected value, per machine where they differ — output you have actually
  seen. A Start here file is those commands and comments, under 10 KB; each how-to paragraph in it moves to the project doc it
  belongs in (one that exists, or a new one under `docs/`), leaving a
  one-line pointer in its place.
- **Landed, and why** — one line per change or decision, about 30 words:
  what changed, then its reason if the reason is written nowhere else,
  otherwise where it is written (a commit, a spec or plan section, a doc
  section). Each item closed this session has its line here.
- **Stops here** — one line per item a cold reader would wrongly assume is
  finished, carried or new. Green tests over code nothing calls belong here.
- **Next** — one line per pending action, the first concrete action first.
  An open question keeps its options in its line, or names where they are
  written, so the next session does not re-derive them.

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

Then end the turn, in this order:

1. **The next-step box**, if the harness has one (a wrap-up tool), with the
   recap alone: no question, no buttons. A box that asks a question ends the
   turn, and a closing message after it is never shown.
2. **Then the closing message**, in full: what you parked, what you could not
   verify, and anything left for them. Its last line is your question for
   them, if there is one.

## Red flags

| About to... | Instead |
|---|---|
| "It's one more line, I'll just finish it" | Is the test already written? Green without a design decision? If not — park it. |
| Write "all tests pass" | Run them. Record what they said. |
| Run the suite again before committing | The Start here run is the Verified run. Once. |
| Wait for the Start here run before writing | It runs in the background; write the entry meanwhile. |
| `grep -v` the progress dots out of the Start here output | `cat` it whole. The filter drops result lines too. |
| Read the log, `git log` and `git status` one by one | One command, §2 step 1. |
| Rewrite a slot nothing changed | One line naming the entry that has it. |
| Drop a finished item from Stops here or Next without a word | A Landed line says it is done and where. |
| Point to the old entry instead of listing its open items | One line per item, naming it. |
| Retell the spec, plan or `SETUP.md` in Landed | One line naming where it is written. |
| Trim a file-level pending list to keep the file short | Every item stays until done; then it moves to history verbatim. |
| `gh run watch` until CI finishes | Record the run id as pending; Start here checks it. |
| Leave an untracked scratch file "for them to delete" | Commit it, delete it, or ignore it. A cold session opens a clean tree. |
| Push the branch and stop | Merge to `main`. A branch is not a handover. |
| `pkill -f python` | Find the pid you started. Kill that one. |
| Give next steps as prose only | Prose plus the runnable **Start here** block. |
| Ask the user's question in the next-step box | Ask it as the closing message's last line. The box gets the recap alone; the closing message follows it. |
| Carry an old expected value forward | Today's value only. Older ones are in the log's Verified lines. |
| Delete a procedure to shrink Start here | Move it to its project doc; leave a one-line pointer. |
| Revert unfinished work so `main` stays green | Commit it with the test skipped. Code belongs in the tree, not quoted in a log. |
| "The note says it's open, but the answer is obvious" | Written down as open means open. Park it. |

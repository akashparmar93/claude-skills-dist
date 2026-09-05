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

## 2. Verify before writing anything down

**REQUIRED SUB-SKILL:** verification-before-completion.

Run the project's test, build and lint commands and read the output. The entry
records what you *ran* and what it *said* — never "tests pass" from memory. If
something is broken, the entry says so. A handover that hides a failure costs
the next session more than the failure does.

## 3. Write the entry

Find the file the project already uses — `OPEN.md`, `PROGRESS.md`, a log under
`docs/` — and match its shape and ordering. Read the previous entry first. Only
propose a new file when there is genuinely none, and ask before creating it.

**Every entry fills these slots. A slot with nothing in it says so.**

- **Status** — one sentence. What is done and landed; what is not.
- **Verified** — the exact commands run and their exact results, dated.
- **Start here** — the block a cold session pastes first: get current, get
  running, confirm green. Run it yourself before you write it down; "expected
  output" means output you have actually seen.
- **Landed, and why** — what changed, plus the decisions made this session and
  their reasons. These exist nowhere else.
- **Stops here** — what a cold reader would wrongly assume is finished. Green
  tests over code nothing calls belong here.
- **Next** — the first concrete action. Open questions list their options, so
  the next session does not re-derive them.

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
| Leave an untracked scratch file "for them to delete" | Commit it, delete it, or ignore it. A cold session opens a clean tree. |
| Push the branch and stop | Merge to `main`. A branch is not a handover. |
| `pkill -f python` | Find the pid you started. Kill that one. |
| Give next steps as prose only | Prose plus the runnable **Start here** block. |
| Revert unfinished work so `main` stays green | Commit it with the test skipped. Code belongs in the tree, not quoted in a log. |
| "The note says it's open, but the answer is obvious" | Written down as open means open. Park it. |

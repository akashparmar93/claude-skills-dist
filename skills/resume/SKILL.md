---
name: resume
description: Use when starting a session on a project that may have moved on — "pull the latest", "get up to date", "where are we", "what's next", "what open items / pending issues", "let's resume", "carry on", "continue on this project" — especially when work happens on more than one machine.
---

# Resume

## Overview

The last session may have run on another machine, and this one may hold work
no other machine has seen. **Find out where you are and what is here, then
report and let the user decide.** A resume reads: it does not reconcile
history, resolve conflicts, run the project, or edit the handover.

## 1. Which machine

`scutil --get ComputerName` (or `hostname`). Read the latest handover entry
(`PROGRESS.md`, `OPEN.md` or `CLAUDE.md`, whichever the project uses) and find
the machine it was verified on.

- Different machine: say so first. Check each one-machine fact the entry
  states (a file, a linked CLI, a tool on `PATH`) with a read, not a run.
- The entry names no machine: say so, and treat its machine facts as
  unconfirmed here.

## 2. What is on this machine only — before pulling

`git status`, `git log @{u}..` after `git fetch`, `git stash list`,
`git branch`, `git worktree list`. Anything found is reported as "on this
machine only". Repeat for every repo the entry's Start here names.

## 3. Get current: fast-forward or stop

`git pull --ff-only`. If it refuses, **stop and report why**:

- Diverged (this machine has unpushed commits, the remote has new ones): show
  both sides and ask how to reconcile.
- Uncommitted changes block it: name the files and ask.

**Never merge, rebase, stash, reset or hand-resolve a conflict unasked.**
Unpushed commits and uncommitted edits are the user's to rewrite.

## 4. Open items

The entry's Next, Stops here and anything left for the owner. Then
`gh pr list` **and** `gh issue list`. If `gh` fails, say GitHub was not
checked and carry on.

## 5. Report, then offer

Four groups, in this order, every item tagged with its source (entry, PR #,
issue #, local git):

1. **This machine** — name, mismatch, facts that do not hold here, local-only
   work.
2. **Waiting on you** — questions only the user can answer; their answers
   change what is next.
3. **Looks done but isn't** — from Stops here.
4. **Next** — the entry's next actions in its order, then open PRs and issues.

Then show the Start here block and offer to run it. Until it runs, nothing is
"passing".

## Red flags

| About to... | Instead |
|---|---|
| "Different files, so I'll rebase — nothing is lost" | It rewrites the user's commit. Stop and ask. |
| Stash, pull, pop, and merge the clash by hand | Name the blocking files. Ask. |
| Run the tests "to check the baseline" | Show Start here and offer. |
| List PRs only | PRs and issues. |

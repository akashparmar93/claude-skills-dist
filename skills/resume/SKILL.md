---
name: resume
description: Use when starting a session on a project that may have moved on — "pull the latest", "get up to date", "where are we", "what's next", "what open items / pending issues", "let's resume", "carry on", "continue on this project" — especially when work happens on more than one machine.
---

# Resume

## Overview

The last session may have run on another machine, and this one may hold work
no other machine has seen. **Find out where you are and what is here, get
current only by fast-forward, then report.** A resume does not reconcile
history, resolve conflicts or edit the handover.

## 1. Read everything in one round

Send these together — one shell call or parallel calls, never one at a time:

- `scutil --get ComputerName` (or `hostname`)
- `git fetch`, then `git status`, `git log --branches --not --remotes`,
  `git stash list`, `git branch -vv`, `git worktree list`
- `gh pr list` and `gh issue list`
- the latest handover entry (`PROGRESS.md`, `OPEN.md` or `CLAUDE.md`,
  whichever the project uses)

Repeat the git reads for every repo the entry's Start here names.

## 2. Which machine, and what is here only

- Entry verified on a different machine: say so first. Check each
  one-machine fact it states (a file, a linked CLI, a tool on `PATH`) with a
  read, not a run.
- The entry names no machine: say so, and treat its machine facts as
  unconfirmed here.
- Uncommitted, unpushed or stashed work is reported as "on this machine only".

## 3. Get current: fast-forward or stop

`git pull --ff-only`. If it refuses, **stop and report why**:

- Diverged (this machine has unpushed commits, the remote has new ones): show
  both sides and ask how to reconcile.
- Uncommitted changes block it: name the files and ask.

**Never merge, rebase, stash, reset or hand-resolve a conflict unasked.**
Unpushed commits and uncommitted edits are the user's to rewrite.

## 4. Report

Four groups, in this order, every item tagged with its source (entry, PR #,
issue #, local git). If `gh` failed, say GitHub was not checked.

1. **This machine** — name, mismatch, facts that do not hold here, local-only
   work.
2. **Waiting on you** — questions only the user can answer; their answers
   change what is next.
3. **Looks done but isn't** — from Stops here.
4. **Next** — the entry's next actions in its order, then open PRs and issues.

## 5. Start here: run it or offer it

**Run it** when the pull fast-forwarded or had nothing new, **and** step 2
found nothing on this machine only. Run it in the background where the
harness allows, send the report without waiting, then give the result. Skip
its get-current lines (the pull is done). At the first failing line, stop and
report the line and its output; do not fix it.

**Otherwise show it and offer.** Until it runs, nothing is "passing".

## Red flags

| About to... | Instead |
|---|---|
| "Different files, so I'll rebase — nothing is lost" | It rewrites the user's commit. Stop and ask. |
| Stash, pull, pop, and merge the clash by hand | Name the blocking files. Ask. |
| Run Start here after a refused pull, or with local-only work | Show it and offer. |
| Run the block's own `git pull` or `checkout` | The pull is done. Run the rest. |
| List PRs only | PRs and issues. |

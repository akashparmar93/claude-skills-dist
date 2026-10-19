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
  Unpushed commits on a branch checked out in another worktree
  (`git worktree list`) are a worktree, not unpushed work: name its path and
  branch.

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

**Nothing runs** after a refused pull, or when step 2 found uncommitted,
stashed or unpushed work: show the block and offer it. Worktrees, and the
unpushed commits on their branches, aren't local-only work.

Otherwise, in this order. No tier headings means the whole block is Full.
Send all output to a file and read it whole, never through `tail`, `head`,
`grep` or `sed`. At the first failing line, stop and report it with its
output; don't fix it.

1. **Every resume:** run it in the foreground, minus `git pull` (done).
2. **Decide Full.** `<sha>` is the latest Verified line's `` at `<sha>` ``.
   Run Full if any box is ticked:
   - [ ] This machine differs from Verified's (case-folded, `’` read as `'`).
   - [ ] No `<sha>`, or `git cat-file -e <sha>` fails.
   - [ ] `git diff --name-only <sha> HEAD` lists a path not ending in `.md`
     (a `.sh` under `docs/` is code).
   - [ ] Verified reports a failure, or "Not verified:" something Full covers.
   - [ ] Verified's date is more than 7 days before today.

   No box ticked: skip Full. Commits touching only `.md` files, the handover
   or another machine's, tick no box.
3. **Full:** run it in the background; send the report, then its result.
4. **Check line**, one in the report:
   - Skipped: "Checks: quick passed on Akash's Mac Studio; full skipped,
     verified on Akash's Mac Studio at `c155cd3`, docs-only since."
   - Ran: "Checks: all passed on Akash's MacBook Air (full ran: other Mac
     last verified)."
   - Failed: "Checks: `make test` failed on Akash's Mac Studio:", then
     its output.

**Cloud session:** always run Full; skip lines marked `# needs a real Mac`
and say so in the check line. **On demand** runs only when Next names it.

## Red flags

| About to... | Instead |
|---|---|
| "Different files, so I'll rebase — nothing is lost" | It rewrites the user's commit. Stop and ask. |
| Stash, pull, pop, and merge the clash by hand | Name the blocking files. Ask. |
| Run Start here after a refused pull, or with local-only work | Show it and offer. |
| Run the block's own `git pull` or `checkout` | The pull is done. Run the rest. |
| List PRs only | PRs and issues. |
| Ran Full on the same Mac with only docs changed | No box ticked: skip Full and say so in the check line. |
| Said checks pass when Full was skipped | Say Full was skipped, naming the Verified machine and sha. |
| Skipped Full because the change looks small | Any path not ending in `.md` ticks the box. Run Full. |
| Treated a worktree as local-only work | Worktrees neither block the checks nor trigger Full. |

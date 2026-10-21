#!/usr/bin/env python3
"""SessionStart hook: bring this machine up to date with the skills repo.

At the start of every session on a Mac this pulls the repo it lives in
(fast-forward only) and runs `skillctl sync`, so both Macs stay current with
no action from the owner. Cloud sessions have bin/cloud-sync.sh for this, so
here it does nothing when CLAUDE_CODE_REMOTE is "true". SKILLCTL_NO_AUTOSYNC
turns it off (`skillctl eval` sets it for its headless runs).

It runs unattended in every repo the owner opens, so it never touches their
work: it only pulls when the checkout is on `main` with an upstream, clean and
not ahead, and the pull is --ff-only. A pull that fails with `cannot lock
ref` (another fetch moved origin/main at the same moment) is tried once more.
Every child (git and the sync) runs in
a session of its own with stdin from /dev/null and GIT_TERMINAL_PROMPT=0, so
neither git nor ssh can prompt, and is bounded by a timeout that kills its
whole process group. One session at a time, by a non-blocking lock.

The outcome is recorded in ~/.claude/skillctl-state.json as
`autosync = {"at": <iso>, "result": <str>}`, which `skillctl status` reports.
Success prints nothing. A skip or failure prints one JSON object,
{"systemMessage": "skillctl: <result>"}, which Claude Code shows the owner:
plain stdout from a SessionStart hook would go to the model's context
instead. Always exits 0. Stdlib only; runs on Python 3.13+.
"""

import datetime
import fcntl
import json
import os
import signal
import subprocess
import sys
import time

# Worst case, every child timing out: six local git calls, the pull and the
# sync, 6 * 3 + 10 + 30 = 58 seconds, inside Claude Code's 60 for a hook.
# A pull retried after losing the ref race shares its 10 with the first try.
PULL_TIMEOUT = 10  # seconds
SYNC_TIMEOUT = 30
GIT_TIMEOUT = 3    # the local, read-only git calls

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Failed(Exception):
    """A step failed; str() is the `failed: <step>: <reason>` result."""


def reason(proc, last=False):
    """First non-empty line of stderr (git names the cause first), or with
    `last` the last one (a Python traceback names its exception last), else
    the exit code."""
    lines = [ln.strip() for ln in (proc.stderr or "").splitlines() if ln.strip()]
    if not lines:
        return "exit %d" % proc.returncode
    return lines[-1] if last else lines[0]


def run(step, cmd, timeout, env=None):
    """Run cmd in a session of its own, so it has no controlling terminal: ssh
    under git cannot open /dev/tty for a passphrase or host-key prompt, and so
    cannot write one into the Claude Code TUI. On a timeout the whole process
    group is killed, so no ssh or `claude plugin` grandchild outlives it."""
    try:
        proc = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True, env=env,
                                start_new_session=True)
    except OSError as e:
        raise Failed("failed: %s: %s" % (step, e.strerror or e))
    with proc:
        try:
            out, err = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except OSError:
                pass
            proc.wait()  # reap; leaving the with-block closes the pipes
            raise Failed("failed: %s: timed out" % step)
    return subprocess.CompletedProcess(cmd, proc.returncode, out, err)


def git(repo, *args, step="git", timeout=GIT_TIMEOUT):
    # No prompt for credentials, and `status` must not take the index lock
    # out from under a git command the owner is running in this checkout.
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "GIT_OPTIONAL_LOCKS": "0"}
    return run(step, ["git", "-C", repo] + list(args), timeout, env)


def git_out(repo, *args):
    """stdout of a git call that must succeed."""
    proc = git(repo, *args)
    if proc.returncode != 0:
        raise Failed("failed: git: %s" % reason(proc))
    return proc.stdout.strip()


def update(repo):
    """Pull and sync; the result string to record."""
    branch = git_out(repo, "rev-parse", "--abbrev-ref", "HEAD")
    if branch != "main":
        return "skipped: on branch %s" % branch
    if git(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}").returncode != 0:
        return "skipped: no upstream"
    if git_out(repo, "status", "--porcelain"):
        return "skipped: uncommitted changes"
    if int(git_out(repo, "rev-list", "--count", "@{u}..HEAD") or 0) > 0:
        return "skipped: local commits"

    old = git_out(repo, "rev-parse", "HEAD")
    start = time.monotonic()
    proc = git(repo, "pull", "--ff-only", "--quiet", step="pull", timeout=PULL_TIMEOUT)
    if proc.returncode != 0 and "cannot lock ref" in (proc.stderr or ""):
        # Another fetch (a session's own `git fetch`) moved the remote-tracking
        # ref under this one. Try once more, inside the same budget.
        proc = git(repo, "pull", "--ff-only", "--quiet", step="pull",
                   timeout=PULL_TIMEOUT - (time.monotonic() - start))
    if proc.returncode != 0:
        return "failed: pull: %s" % reason(proc)
    new = git_out(repo, "rev-parse", "HEAD")

    proc = run("sync", [sys.executable, os.path.join(repo, "bin", "skillctl"), "sync"],
               SYNC_TIMEOUT)
    if proc.returncode != 0:
        return "failed: sync: %s" % reason(proc, last=True)
    return "pulled %s..%s" % (old[:7], new[:7]) if new != old else "up to date"


def record(home, result):
    """Merge `autosync` into the skillctl state file, keeping every other key."""
    path = os.path.join(home, ".claude", "skillctl-state.json")
    try:
        with open(path) as f:
            state = json.load(f)
        if not isinstance(state, dict):
            state = {}
    except (OSError, ValueError):
        state = {}
    at = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    state["autosync"] = {"at": at, "result": result}
    try:
        with open(path, "w") as f:
            json.dump(state, f, indent=2)
    except OSError:
        pass


def main(repo=REPO) -> int:
    if os.environ.get("CLAUDE_CODE_REMOTE") == "true" or "SKILLCTL_NO_AUTOSYNC" in os.environ:
        return 0
    home = os.path.expanduser("~")
    try:
        os.makedirs(os.path.join(home, ".claude"), exist_ok=True)
        lock = open(os.path.join(home, ".claude", "skillctl-autosync.lock"), "a")
    except OSError:
        return 0
    with lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            return 0  # another session is already syncing
        try:
            result = update(repo)
        except Failed as e:
            result = str(e)
        record(home, result)
    if not result.startswith(("pulled ", "up to date")):
        sys.stdout.write(json.dumps({"systemMessage": "skillctl: " + result}))
    return 0


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)

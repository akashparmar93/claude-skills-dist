#!/usr/bin/env python3
"""UserPromptSubmit hook: warn the owner, once per session, that the
auto-loaded instruction files are large.

Claude Code re-sends these files on every turn, so their total size is a
standing cost. On the first prompt of a session this measures:

  - CLAUDE.md and CLAUDE.local.md in cwd and each parent (up to and including
    $HOME when cwd is under it, else up to /)
  - <cwd>/.claude/CLAUDE.md
  - ~/.claude/CLAUDE.md
  - the auto-memory index, ~/.claude/projects/<cwd, every non-alphanumeric
    character replaced by "-">/memory/MEMORY.md

AGENTS.md is not listed: Claude Code does not auto-load it. Symlinks are
followed and a file reached twice counts once.

Known gap: `@path` imports inside CLAUDE.md are not followed.

Emits {"systemMessage": ...} only. Plain stdout from a UserPromptSubmit hook
is added to the model's context, so this prints nothing or exactly one JSON
object, and never additionalContext. Fail silent: any error, missing file or
unparseable input means no output and exit 0.

Markers live at <home>/.claude/state/size-warn/<session_id>. One is written
for every session on its first prompt, warned or not, so the files are
measured once. Stdlib only; runs on Python 3.9.
"""

import json
import os
import re
import sys
import time
from typing import List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import markers  # noqa: E402  (shared marker code, next to this file)

THRESHOLD = 20480
BYTES_PER_TOKEN = 3
MARKER_TTL = 14 * 86400
ADVICE = "Consider moving history to a log that isn't auto-loaded."


def memory_index(cwd: str, home: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]", "-", cwd)
    return os.path.join(home, ".claude", "projects", slug, "memory", "MEMORY.md")


def _under(path: str, root: str) -> bool:
    return path == root or path.startswith(root.rstrip(os.sep) + os.sep)


def auto_loaded_files(cwd: str, home: str) -> List[str]:
    """Existing auto-loaded files, each real file once, in load order."""
    candidates = []  # type: List[str]
    stop_at_home = _under(cwd, home)
    d = cwd
    while True:
        candidates.append(os.path.join(d, "CLAUDE.md"))
        candidates.append(os.path.join(d, "CLAUDE.local.md"))
        parent = os.path.dirname(d)
        if (stop_at_home and d == home) or parent == d:
            break
        d = parent
    candidates.append(os.path.join(cwd, ".claude", "CLAUDE.md"))
    candidates.append(os.path.join(home, ".claude", "CLAUDE.md"))
    candidates.append(memory_index(cwd, home))

    seen = set()
    found = []
    for path in candidates:
        if not os.path.isfile(path):
            continue
        real = os.path.realpath(path)
        if real not in seen:
            seen.add(real)
            found.append(path)
    return found


def _display(path: str, cwd: str, home: str) -> str:
    if path.startswith(cwd.rstrip(os.sep) + os.sep):
        return os.path.relpath(path, cwd)
    if path.startswith(home.rstrip(os.sep) + os.sep):
        return "~/" + os.path.relpath(path, home)
    return path


def _kb(size: int) -> str:
    return "%d KB" % round(size / 1024)


def _tokens(size: int) -> str:
    return "~%dk tokens" % round(size / BYTES_PER_TOKEN / 1000)


def message(cwd: str, home: str) -> Optional[str]:
    sizes = [(os.path.getsize(p), p) for p in auto_loaded_files(cwd, home)]
    total = sum(s for s, _ in sizes)
    if total <= THRESHOLD:
        return None
    big_size, big_path = max(sizes, key=lambda sp: sp[0])
    name = _display(big_path, cwd, home)
    if len(sizes) == 1:
        return "⚠ %s is %s (%s re-sent on every turn). %s" % (
            name, _kb(big_size), _tokens(big_size), ADVICE)
    return ("⚠ Auto-loaded instruction files total %s (%s re-sent on every turn); "
            "the largest is %s at %s. %s" % (
                _kb(total), _tokens(total), name, _kb(big_size), ADVICE))


def main(stdin_text: str, home: str, now: float) -> str:
    data = json.loads(stdin_text)
    session = data.get("session_id")
    if not isinstance(session, str) or not session or os.path.basename(session) != session:
        return ""
    state_dir = os.path.join(home, ".claude", "state", "size-warn")
    markers.expire(state_dir, now, MARKER_TTL)
    cwd = data.get("cwd")
    if not isinstance(cwd, str) or not os.path.isdir(cwd):
        return ""
    marker = os.path.join(state_dir, session)
    if os.path.exists(marker):
        return ""
    msg = message(cwd, home)
    if not markers.mark(marker) or msg is None:
        return ""
    return json.dumps({"systemMessage": msg})


if __name__ == "__main__":
    try:
        out = main(sys.stdin.read(), os.path.expanduser("~"), time.time())
        if out:
            sys.stdout.write(out)
    except Exception:
        pass
    sys.exit(0)

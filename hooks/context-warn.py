#!/usr/bin/env python3
"""Stop hook: tell the owner, once per threshold, that a session's context is large.

Context is input_tokens + cache_read_input_tokens + cache_creation_input_tokens
of the last main-thread assistant record in the transcript. The transcript is
read backwards in 64 KB blocks, so a 40 MB file costs one or two reads.

Emits {"systemMessage": ...} only: never additionalContext (the model is not
told) and never decision (the stop is never blocked). Fail silent: any error,
missing file or unparseable input means no output and exit 0.

Markers live at <home>/.claude/state/context-warn/<session_id>.<threshold>.
Stdlib only; runs on Python 3.9.
"""

import json
import os
import sys
import time
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import markers  # noqa: E402  (shared marker code, next to this file)

THRESHOLDS = (200000, 400000)
BLOCK = 65536
SCAN_LIMIT = 4 * 1024 * 1024
MARKER_TTL = 14 * 86400

_USAGE = b'"usage"'


def _record_size(line: bytes) -> Optional[int]:
    """Context size if `line` is a qualifying assistant record, else None."""
    if _USAGE not in line:
        return None
    try:
        rec = json.loads(line)
        if rec.get("type") != "assistant" or rec.get("isSidechain"):
            return None
        usage = rec["message"]["usage"]
        total = ((usage.get("input_tokens") or 0)
                 + (usage.get("cache_read_input_tokens") or 0)
                 + (usage.get("cache_creation_input_tokens") or 0))
    except Exception:
        return None
    return total if isinstance(total, int) and total > 0 else None


def context_size(transcript_path: str) -> Optional[int]:
    """Context of the last qualifying record, or None (none found, or SCAN_LIMIT hit)."""
    with open(transcript_path, "rb") as f:
        pos = f.seek(0, os.SEEK_END)
        carry = b""
        scanned = 0
        while pos > 0 and scanned < SCAN_LIMIT:
            start = max(0, pos - BLOCK)
            f.seek(start)
            chunk = f.read(pos - start)
            scanned += len(chunk)
            pos = start
            lines = (chunk + carry).split(b"\n")
            if start > 0:
                carry, lines = lines[0], lines[1:]  # first line may be cut off
            else:
                carry = b""
            for line in reversed(lines):
                size = _record_size(line)
                if size is not None:
                    return size
    return None


def main(stdin_text: str, home: str, now: float) -> str:
    data = json.loads(stdin_text)
    session = data.get("session_id")
    if not isinstance(session, str) or not session or os.path.basename(session) != session:
        return ""
    state_dir = os.path.join(home, ".claude", "state", "context-warn")
    markers.expire(state_dir, now, MARKER_TTL)

    tokens = context_size(data.get("transcript_path"))
    if tokens is None:
        return ""

    def marker(threshold: int) -> str:
        return os.path.join(state_dir, "%s.%d" % (session, threshold))

    reached = [t for t in THRESHOLDS if tokens >= t]
    fresh = [t for t in reached if not os.path.exists(marker(t))]
    if not fresh:
        return ""
    highest = max(fresh)
    if not all([markers.mark(marker(t)) for t in reached if t <= highest]):
        return ""
    return json.dumps({"systemMessage": (
        "ⓘ This session's context is at %dk tokens. Every turn re-sends all of it; "
        "a handover and a fresh session would reset it." % (tokens // 1000))})


if __name__ == "__main__":
    try:
        out = main(sys.stdin.read(), os.path.expanduser("~"), time.time())
        if out:
            sys.stdout.write(out)
    except Exception:
        pass
    sys.exit(0)

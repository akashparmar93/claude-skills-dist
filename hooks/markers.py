"""Marker files shared by the warn-only hooks (context-warn.py, size-warn.py).

A marker is an empty file whose existence means "already warned". It is written
before a message is shown, so a failed write means the hook stays silent rather
than repeating itself on every run. Stdlib only; runs on Python 3.13+.
"""

import os


def expire(state_dir: str, now: float, ttl: float) -> None:
    """Delete files in `state_dir` last modified more than `ttl` seconds before `now`."""
    try:
        names = os.listdir(state_dir)
    except OSError:
        return
    for name in names:
        path = os.path.join(state_dir, name)
        try:
            if os.stat(path).st_mtime < now - ttl:
                os.remove(path)
        except OSError:
            pass


def mark(path: str) -> bool:
    """Create the marker (and its directory). False if that could not be done."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "a").close()
    except OSError:
        return False
    return True

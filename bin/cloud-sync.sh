#!/bin/bash
# SessionStart hook for Claude Code cloud sessions.
#
# Refreshes ~/.claude/claude-skills from the public mirror and re-runs
# `skillctl sync`, so every cloud session — in any repo, on any device —
# starts with the current skills.
#
# Verified 2026-08-21: skills installed by a SessionStart hook ARE registered
# in the same session. A probe skill written by this kind of hook appeared in
# the session's init `skills` array and was invoked through the Skill tool.
# So this hook is sufficient on its own; the setup script only bootstraps it.
#
# Silent and non-fatal by design: a session must still start if GitHub is
# unreachable. Failures land in the log rather than blocking the session.
set -uo pipefail

DIR="${SKILLCTL_CLOUD_DIR:-$HOME/.claude/claude-skills}"
MIRROR="${SKILLCTL_MIRROR:-https://github.com/akashparmar93/claude-skills-dist}"
LOG="$HOME/.claude/skillctl-cloud.log"

log() { printf '%s  %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" >>"$LOG" 2>/dev/null || true; }

# Only manage the container's skills. On a real device the skills come from the
# private repo via SETUP.md, and this must never touch them.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

if [ -d "$DIR/.git" ]; then
  if git -C "$DIR" fetch --quiet --depth 1 origin main 2>>"$LOG"; then
    git -C "$DIR" reset --hard --quiet FETCH_HEAD 2>>"$LOG" || log "reset failed"
  else
    log "fetch failed — using the clone already on disk"
  fi
else
  # Self-heal: the environment cache may predate this hook, or have been wiped.
  rm -rf "$DIR"
  git clone --quiet --depth 1 "$MIRROR" "$DIR" 2>>"$LOG" || { log "clone failed — no skills installed"; exit 0; }
fi

if out=$("$DIR/bin/skillctl" sync --force 2>&1); then
  log "synced $(git -C "$DIR" rev-parse --short HEAD 2>/dev/null)"
else
  log "sync failed: $out"
fi

exit 0

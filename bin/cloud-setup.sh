#!/bin/bash
# Bootstrap Claude Code cloud sessions with the skills from the public mirror.
#
# This is the payload behind the one-time setup script you paste into
# claude.ai -> Cloud environments -> Default. It runs once per environment
# cache generation, before Claude Code launches, and its whole job is to make
# the per-session hook exist:
#
#   1. clone the public mirror to ~/.claude/claude-skills
#   2. register bin/cloud-sync.sh as a user-level SessionStart hook
#   3. run one sync, so the very first session is already correct
#
# Everything after that is the hook's job. Keeping the logic here — rather
# than in the pasted script — means changes ship by publishing the mirror
# instead of by re-pasting into the environment dialog.
set -euo pipefail

DIR="${SKILLCTL_CLOUD_DIR:-$HOME/.claude/claude-skills}"
MIRROR="${SKILLCTL_MIRROR:-https://github.com/akashparmar93/claude-skills-dist}"
SETTINGS="$HOME/.claude/settings.json"

if [ -d "$DIR/.git" ]; then
  git -C "$DIR" fetch --quiet --depth 1 origin main && git -C "$DIR" reset --hard --quiet FETCH_HEAD
else
  rm -rf "$DIR"
  git clone --quiet --depth 1 "$MIRROR" "$DIR"
fi
chmod +x "$DIR/bin/skillctl" "$DIR/bin/cloud-sync.sh" 2>/dev/null || true

# Register the hook in user settings, merging rather than overwriting: the
# container may already carry hooks, and re-running must not duplicate ours.
mkdir -p "$HOME/.claude"
HOOK="$DIR/bin/cloud-sync.sh" python3 - "$SETTINGS" <<'PY'
import json, os, sys

path, hook = sys.argv[1], os.environ["HOOK"]
try:
    with open(path) as f:
        settings = json.load(f)
except (FileNotFoundError, ValueError):
    settings = {}

hooks = settings.setdefault("hooks", {})
groups = hooks.setdefault("SessionStart", [])

def registered(entry):
    return any(h.get("command") == hook for h in entry.get("hooks", []))

if any(registered(g) for g in groups):
    print("SessionStart hook already registered")
else:
    groups.append({"hooks": [{"type": "command", "command": hook}]})
    with open(path, "w") as f:
        json.dump(settings, f, indent=2)
        f.write("\n")
    print("registered SessionStart hook -> %s" % hook)
PY

CLAUDE_CODE_REMOTE=true "$DIR/bin/skillctl" sync --force

echo
echo "cloud bootstrap complete — $(git -C "$DIR" rev-parse --short HEAD)"

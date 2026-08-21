# claude-skills-dist

Public, generated distribution of my Claude Code skills. **Do not edit or open
pull requests here** — this repo is overwritten wholesale by `skillctl publish`
from a private source repo, so any change made here is lost on the next publish.

It exists for one reason: a Claude Code cloud session working in some *other*
repo cannot clone a private one (the session's git credentials are scoped to
the repos attached to that session), so the skills have to be reachable
without authentication.

## What a cloud session does with this

```bash
git clone --depth 1 https://github.com/akashparmar93/claude-skills-dist ~/.claude/claude-skills
~/.claude/claude-skills/bin/cloud-setup.sh
```

`cloud-setup.sh` registers `bin/cloud-sync.sh` as a user-level SessionStart
hook, which re-pulls this repo and re-runs `skillctl sync` at the start of
every session. Skills installed that way are registered in the same session.

## Contents

`skills/` — 21 skills, `skills.json` — the manifest they are pinned by,
`CLAUDE.md` — the routing table that makes them fire, `bin/skillctl` — the
sync tool, `bin/cloud-*.sh` — the cloud bootstrap and hook.

Most of the skills are vendored from public upstreams; `skills.json` records
each one's origin repo and pinned commit. Credit belongs to their authors.

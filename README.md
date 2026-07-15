# memory-carryover

A Claude Code plugin that makes per-project memory survive context compaction and stay
cheap. It fixes the common complaint: "Claude said it saved something to memory, but after
a while it forgot it anyway."

You enable it once. After that it works on its own: hooks re-inject your memory every
session and after every compaction, and a bundled skill teaches Claude how to keep that
memory lean and reliable.

## Requirements

- **Python 3** must be installed and on your PATH (the hooks and the audit are Python
  scripts). Check with `python3 --version`. If it is missing, install it from python.org
  and tick "Add to PATH", or on Windows from the Microsoft Store, which provides
  `python3`. Run `/memory-doctor` after install to confirm.
- **Git** is optional. If it is present, the PreCompact hook adds a small read-only git
  snapshot (branch, uncommitted files, last commits) to the saved state. Without git, the
  snapshot just records the working directory and time. The hooks only read git and never
  write to it.
- Works on Linux, macOS, and Windows.

## What it does

Claude Code stores per-project memory at `~/.claude/projects/<project-slug>/memory/`: a
`MEMORY.md` index plus one file per fact. The problem is that "saved" is not "recalled" -
a fact only comes back into context if the recall step fires, and after a compaction the
index may not be re-injected at all. memory-carryover closes that gap.

- **SessionStart hook** re-injects the current project's `MEMORY.md`, `STATUS.md`, and
  `COMPACT-SNAPSHOT.md` into context on startup, resume, clear, and right after every
  compaction. So the index and live status are always back in front of the model.
- **PreCompact hook** reads a small git snapshot (branch, uncommitted files, last commits)
  and writes it to disk before compaction, so mechanical state survives and gets
  re-injected. It only reads git; git is optional and is never modified.
- **Memory maintenance skill** (`memory-maintenance`) teaches Claude how to keep the index
  lean: bulky reference goes in on-demand topic files, short critical rules stay inline,
  current state lives in `STATUS.md`, and every fact stays linked so it recalls.
- **Slash commands**: `/memory-audit` (report problems), `/memory-tidy` (clean the current
  project's memory), `/memory-doctor` (health check: Python, hooks, memory dir).

Only the small index-level files are injected each session, so the per-session token cost
stays low. Bulky detail loads on demand.

## Install

```text
/plugin marketplace add mishasaz/memory-carryover
/plugin install memory-carryover@mishasaz
```

Then restart Claude Code, or open the `/hooks` menu once, so the hooks activate. Claude
Code snapshots hooks at startup, so they do not apply to the already-running session.

Run `/memory-doctor` to confirm Python is available and the hooks are registered.

(The GitHub repo must be named `memory-carryover` under your account for the
`marketplace add` line above to match. Rename the repo or the command accordingly.)

## Usage

- Nothing is required day to day. As you work, keep each active project's `STATUS.md`
  current (now / next / blockers). The skill and `/memory-tidy` help Claude do this.
- Run `/memory-audit` occasionally to catch memory that stopped working (orphaned facts,
  oversized indexes).
- Run `/memory-tidy` when a project's `MEMORY.md` has grown large, to unload bulky
  reference into topic files while keeping critical rules inline.

## How the memory method works

The skill (`skills/memory-maintenance/SKILL.md`) is the full method. In short:

- `MEMORY.md` is an index: one line per fact with a strong keyword hook, links to topic
  files for detail. It is injected every session, so keep it lean.
- `STATUS.md` holds volatile state (now / next / blockers / do-not-touch). It is the thing
  most often lost after a compaction, so it is injected too.
- topic files hold bulky reference and load on demand via recall. Every one must be linked
  from `MEMORY.md`, or it is invisible.
- A fact with no index line never recalls. The audit flags these.

## Layout

```text
memory-carryover/
  .claude-plugin/
    plugin.json
    marketplace.json
  hooks/
    hooks.json
    inject_memory.py
    precompact_snapshot.py
  skills/
    memory-maintenance/
      SKILL.md
  commands/
    memory-audit.md
    memory-tidy.md
    memory-doctor.md
  scripts/
    mem_audit.py
  README.md
  LICENSE
```

## Notes and caveats

- Hooks activate after a restart or one open of `/hooks`, not mid-session.
- The hooks find the project memory dir from the hook's `transcript_path`, so they work
  per-project with no configuration.
- PreCompact can only capture mechanical (git) state. Semantic state is kept in `STATUS.md`
  by you or the model.
- Nothing here is destructive on its own. The audit only reports. Tidying moves facts
  (verbatim) and occasionally deletes verified duplicates, so review before deleting.

## Donate

If this saved you some tokens, a tip is welcome.

USDT (BEP-20): `0x7e5db543734E5BD59E0df1B27820A1EAF2BE438B`

## License

MIT. Do whatever you want with it.

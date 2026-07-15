---
name: memory-maintenance
description: >-
  How to maintain Claude Code per-project memory so it survives context compaction and
  stays token-cheap. Use when creating, organizing, auditing, or cleaning a project's
  memory files (the MEMORY.md index, STATUS.md, per-fact topic files), when a project's
  MEMORY.md has grown large, or when the user asks to tidy, unload, or optimize memory.
---

# Memory maintenance

Claude Code keeps per-project memory at `~/.claude/projects/<project-slug>/memory/`: a
`MEMORY.md` index plus one file per fact. This skill is the procedure for keeping that
memory reliable and cheap. It pairs with the plugin's SessionStart hook, which injects
`MEMORY.md`, `STATUS.md`, and `COMPACT-SNAPSHOT.md` into context every session and after
every compaction.

## The core rule

"Saved" is not "recalled". A fact is only recalled if a one-line pointer to it exists in
`MEMORY.md`, because recall matches on those index lines. A fact file with no index line is
invisible. After a compaction the model loses the live transcript, so anything not in an
always-injected file (the index or `STATUS.md`) must be recalled, which is not guaranteed.
Everything below exists to make the important things always-present and the rest reliably
findable.

## The three files

- **MEMORY.md** - the index. One line per fact, each a link plus a keyword-rich hook. It is
  injected every session, so keep it lean.
- **STATUS.md** - volatile state (now / next / blockers / do-not-touch). The thing most
  often lost after a compaction. Injected every session.
- **topic files** (any other `*.md`) - bulky reference, loaded on demand via recall. Each
  must be linked from `MEMORY.md` or it never recalls.

`STATUS.md` and `COMPACT-SNAPSHOT.md` are injected directly by the hook, so they do NOT
need an index line.

## Decide: keep inline in MEMORY.md, or move to a topic file

Keep **inline** (short, needed often, or a guardrail):

- safety rules: "never edit prod .env directly", "never run a build without asking"
- stable identifiers that must not change: "plan slugs are stable: free / basic / pro"
- one-line invariants: "signal lifecycle is price-based, detected in SignalMonitor"

Move to a **topic file** (bulky, needed only when working on that thing):

- schemas, table lists, endpoint lists
- long or multi-step procedures and setup
- deep architecture write-ups

Rule of thumb: if it is more than about two lines and you do not need it every session, it
is a topic file, not an index entry.

## Write a good index line (the recall hook)

The text after the link is what recall matches on. Make it specific and keyword-rich.

- Good: `[deploy.md](deploy.md) - deploy: SSH command, server paths, rsync pattern, restart`
- Bad:  `[deploy.md](deploy.md) - deploy info`

One fact per file; the file name matches the fact.

## STATUS.md

```
# STATUS (volatile state; update as work progresses)

- Now: what we are doing this iteration
- Next: the next concrete step
- Blockers / waiting on: what we are waiting for (client, data, decision)
- Do not touch: anything that must not be changed
- Updated: YYYY-MM-DD
```

Update it at every meaningful checkpoint (a step finished, a blocker hit, focus switched),
not only at session end. If a project is an umbrella of several efforts, give it one block
per live thread. Do not duplicate `STATUS.md` content in `MEMORY.md`.

## Procedure: unload a bloated MEMORY.md

1. Run the audit and note oversized indexes and orphans:
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/mem_audit.py"`
2. For each bulky inline block: cut it VERBATIM into a `<topic>.md` file and replace it with
   one index line (link plus a keyword hook).
3. Keep short critical rules inline (see the decision rules above).
4. Move any "current state / what's next" block into `STATUS.md`. Do not duplicate it.
5. Preserve every fact. Move text verbatim; never reword it away or drop it.
6. Verify: re-run the audit. There must be zero orphans and zero broken links. An index
   that is still over the size flag but consists only of legitimate one-line entries (not
   inline content) is fine.

## Link or delete

- **Orphan** fact (a file with no index line): LINK it. Add an index line. Non-destructive,
  and it fixes recall.
- **Duplicate** fact (its content is already a verbatim inline rule): you may DELETE the
  file, but only after confirming the fact is preserved inline. Show the plan before
  deleting.
- When unsure: link, do not delete.

## Final checklist

- MEMORY.md is an index (one line per fact), not a document.
- Every topic file is linked from MEMORY.md (no orphans).
- Every link resolves (no broken links).
- Critical and safety rules are inline; bulky reference is in topic files.
- Each active project has a current STATUS.md.
- No fact was lost in any move.

---
name: memory-tidy
description: Tidy the current project's Claude Code memory using the balanced lean-index method (unload bulky reference, keep critical inline, fix orphans, refresh STATUS.md).
---

Tidy this project's memory following the `memory-maintenance` skill.

1. Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/mem_audit.py"` to see the current issues.
2. For the current project's `MEMORY.md`:
   - Move bulky reference (schemas, tables, long procedures, architecture detail) into
     on-demand `<topic>.md` files, moving text VERBATIM.
   - Keep short critical/safety rules and stable identifiers inline in `MEMORY.md`.
   - Move any "current state / what's next" block into `STATUS.md` (create it if missing,
     using the template from the skill). Do not duplicate it in the index.
   - Link every orphan fact so it recalls. Only delete a fact if its content is a verbatim
     duplicate of an inline rule, and only after confirming it is preserved.
3. Preserve every fact - never invent, reword away, or drop one.
4. Verify afterward: no orphaned files, no broken links (re-run the audit).
5. Show the plan before deleting anything.

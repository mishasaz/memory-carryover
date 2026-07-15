---
name: memory-audit
description: Run the read-only structural audit of Claude Code project memory and summarize what needs fixing.
---

Run the structural memory audit and report the results:

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/mem_audit.py"
```

If `python3` is not found, try `python` then `py`, and if none work tell the user Python 3
is required (see /memory-doctor).

Then summarize the findings grouped by project: which indexes are empty-with-facts,
oversized, or have orphaned (unlinked) fact files. For each, state the concrete fix from
the memory-maintenance skill (link the orphan, unload the oversized index into topic files,
or delete a verified duplicate). Do not change anything - this command only reports.

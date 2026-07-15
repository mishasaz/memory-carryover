---
name: memory-doctor
description: Check that the memory plugin is healthy - Python is available, hooks are installed, and the memory directory is reachable.
---

Diagnose the memory plugin setup and report a short health check. Run these and interpret:

1. **Python** (required by the hooks and audit). Check, in order, `python3 --version`,
   then `python --version`, then `py --version`. Report which interpreter is available and
   its version. If NONE work, tell the user clearly: "Python 3 is not installed or not on
   PATH. This plugin needs Python 3 - install it from python.org (tick 'Add to PATH') or,
   on Windows, from the Microsoft Store, which provides `python3`." This is the critical
   check - without Python the hooks cannot run.

2. **Hooks registered**: confirm the plugin is enabled and its SessionStart + PreCompact
   hooks are active (mention the user can verify in the `/hooks` menu). Note that hooks
   activate only after a restart or one open of `/hooks`, not mid-session.

3. **Memory directory**: confirm `~/.claude/projects/<current-project-slug>/memory/` is
   reachable and list whether `MEMORY.md` / `STATUS.md` exist for the current project.

4. **Git (optional)**: check `git --version`. If present, say the PreCompact snapshot will
   include git info (branch, uncommitted files, last commits). If absent, that is fine -
   git is optional; the snapshot simply omits git details. The hooks only read git, never
   write to it. This is not a blocker.

Report each as OK or a clear one-line fix. Keep it short.

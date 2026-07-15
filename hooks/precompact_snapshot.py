#!/usr/bin/env python3
"""PreCompact hook. Flush mechanical state (git) to disk before the transcript is
compacted, so inject_memory.py can re-inject it after the compaction. Captures only what
a shell can know; the semantic 'what we're doing / next' is kept by the model in
memory/STATUS.md, not here. Cross-platform."""
import sys, json, os, subprocess
from datetime import datetime


def project_dir_from_stdin():
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except Exception:
        data = {}
    tp = data.get("transcript_path", "")
    if tp:
        d = os.path.dirname(tp)
        if os.path.isdir(d):
            return d
    base = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    slug = base.replace("/", "-").replace("\\", "-").replace(":", "")
    return os.path.join(os.path.expanduser("~"), ".claude", "projects", slug)


def git(cwd, *args):
    try:
        r = subprocess.run(["git", "-C", cwd, *args],
                           capture_output=True, text=True, timeout=8)
        return r.stdout.strip()
    except Exception:
        return ""


def main():
    memdir = os.path.join(project_dir_from_stdin(), "memory")
    try:
        os.makedirs(memdir, exist_ok=True)
    except Exception:
        return
    cwd = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    lines = ["# Compaction snapshot (%s)" % datetime.now().strftime("%Y-%m-%d %H:%M"),
             "cwd: %s" % cwd]
    if git(cwd, "rev-parse", "--git-dir"):
        lines += ["",
                  "branch: %s" % git(cwd, "branch", "--show-current"),
                  "",
                  "## uncommitted (git status --short)",
                  git(cwd, "status", "--short"),
                  "",
                  "## last commits",
                  git(cwd, "log", "--oneline", "-5")]
    try:
        with open(os.path.join(memdir, "COMPACT-SNAPSHOT.md"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
    except Exception:
        pass


if __name__ == "__main__":
    main()

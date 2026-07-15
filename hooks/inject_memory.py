#!/usr/bin/env python3
"""SessionStart hook. Re-inject the current project's memory index + live status into
context on startup / resume / clear / and right after a compaction. Stdout is added to
the model context. Keep output small (index-level only). Cross-platform (no shell deps)."""
import sys, json, os


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
    # Fallback: mangle the project path the way Claude Code forms slugs (sep -> -).
    base = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    slug = base.replace("/", "-").replace("\\", "-").replace(":", "")
    return os.path.join(os.path.expanduser("~"), ".claude", "projects", slug)


def main():
    memdir = os.path.join(project_dir_from_stdin(), "memory")
    if not os.path.isdir(memdir):
        return
    # Only index-level files. Per-fact topic files stay on-demand (recall), not injected.
    for name in ("MEMORY.md", "STATUS.md", "COMPACT-SNAPSHOT.md"):
        path = os.path.join(memdir, name)
        try:
            if os.path.isfile(path) and os.path.getsize(path) > 0:
                with open(path, encoding="utf-8") as fh:
                    body = fh.read()
                print("===== project memory: %s =====" % name)
                sys.stdout.write(body)
                if not body.endswith("\n"):
                    sys.stdout.write("\n")
                print()
        except Exception:
            pass


if __name__ == "__main__":
    main()

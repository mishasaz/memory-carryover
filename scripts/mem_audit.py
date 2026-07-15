#!/usr/bin/env python3
"""Read-only structural audit of Claude Code per-project memory. Cross-platform.

Flags the three ways a saved memory silently stops working:
  1. Empty MEMORY.md that still has fact files -> those facts never recall.
  2. Oversized MEMORY.md (>6KB) -> likely inline content that belongs in topic files
     (MEMORY.md is injected every session).
  3. Fact files not linked from MEMORY.md -> orphans, will never recall.

STATUS.md and COMPACT-SNAPSHOT.md are injected directly by the SessionStart hook, so they
are not expected to be linked from MEMORY.md and are excluded here."""
import os, glob

NONINDEX = {"MEMORY.md", "STATUS.md", "COMPACT-SNAPSHOT.md"}
OVERSIZE = 6144
PROJECTS = os.path.join(os.path.expanduser("~"), ".claude", "projects")


def fact_files(memdir):
    return [os.path.basename(p) for p in glob.glob(os.path.join(memdir, "*.md"))
            if os.path.basename(p) not in NONINDEX]


def project_name(md):
    return os.path.basename(os.path.dirname(os.path.dirname(md)))


def main():
    indexes = glob.glob(os.path.join(PROJECTS, "*", "memory", "MEMORY.md"))
    print("=== mem-audit: structural integrity of project memory ===\n")

    print("## Empty MEMORY.md that still have fact files (facts will NOT recall):")
    for md in indexes:
        memdir = os.path.dirname(md)
        facts = fact_files(memdir)
        if os.path.getsize(md) == 0 and facts:
            print("  [%s] empty index, %d orphan fact file(s)" % (project_name(md), len(facts)))
    print()

    print("## Oversized MEMORY.md (>6KB - likely inline content that belongs in topic files):")
    big = [(os.path.getsize(md), md) for md in indexes if os.path.getsize(md) > OVERSIZE]
    for size, md in sorted(big):
        print("  %d bytes  %s" % (size, md))
    print()

    print("## Fact files NOT linked from their MEMORY.md (orphans - will NOT recall):")
    for md in indexes:
        memdir = os.path.dirname(md)
        try:
            text = open(md, encoding="utf-8").read()
        except Exception:
            text = ""
        for base in fact_files(memdir):
            if base not in text:
                print("  [%s] %s" % (project_name(md), base))
    print()
    print("Done. A fact with no index line is invisible to recall - link it or delete it.")


if __name__ == "__main__":
    main()

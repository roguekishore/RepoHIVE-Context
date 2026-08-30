#!/usr/bin/env python3
"""Generate decisions/README.md from the frontmatter of every decision file.

Run this after adding, editing, or renaming any decision file:

    python gen-index.py <decisions-dir>

The index is GENERATED. Never hand-edit it: a hand-written index is a second
home for the same fact, and the two drift. Every value below is read from the
files themselves, so the index cannot disagree with them.

Exits non-zero on any structural problem (missing field, dangling
superseded_by, filename not matching date-slug), so it doubles as a check.
"""

import glob
import io
import os
import re
import sys
from collections import defaultdict

FIELDS = ("date", "slug", "title", "status", "superseded_by", "supersedes",
          "summary", "corrected")


def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
        return v[1:-1]
    return v


def parse_frontmatter(path):
    text = io.open(path, encoding="utf-8").read()
    if not text.startswith("---"):
        raise ValueError("no frontmatter")
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError("unterminated frontmatter")
    block = text[3:end]

    data = {}
    key = None
    for line in block.splitlines():
        if not line.strip():
            continue
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            val = m.group(2)
            # Folded scalar: value continues on following indented lines.
            data[key] = "" if val.strip() in (">", "|") else unquote(val)
        elif key and line.startswith((" ", "\t")):
            data[key] = (data[key] + " " + line.strip()).strip()
    return data


def main():
    if len(sys.argv) < 2:
        print("usage: gen-index.py <decisions-dir>", file=sys.stderr)
        return 2
    d = sys.argv[1]

    paths = sorted(p for p in glob.glob(os.path.join(d, "*.md"))
                   if os.path.basename(p).lower() != "readme.md")
    if not paths:
        print("gen-index: no decision files found in %s" % d, file=sys.stderr)
        return 2

    entries = []
    errors = []
    for p in paths:
        base = os.path.basename(p)
        try:
            fm = parse_frontmatter(p)
        except ValueError as e:
            errors.append("%s: %s" % (base, e))
            continue
        missing = [f for f in FIELDS if f not in fm or fm[f] == ""]
        # superseded_by/supersedes legitimately hold the literal "null".
        missing = [f for f in missing
                   if f not in ("superseded_by", "supersedes")]
        if missing:
            errors.append("%s: missing %s" % (base, ", ".join(missing)))
            continue
        expected = "%s-%s.md" % (fm["date"], fm["slug"])
        if base != expected:
            errors.append("%s: filename should be %s" % (base, expected))
        fm["_file"] = base
        entries.append(fm)

    slugs = {e["slug"] for e in entries}
    for e in entries:
        t = e.get("superseded_by", "null")
        if t and t != "null" and t not in slugs:
            errors.append("%s: superseded_by names unknown slug '%s'"
                          % (e["_file"], t))
        s = e.get("supersedes", "null")
        if s and s != "null" and s not in slugs:
            errors.append("%s: supersedes names unknown slug '%s'"
                          % (e["_file"], s))

    if errors:
        print("gen-index: FAILED", file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)
        return 1

    by_date = defaultdict(list)
    for e in entries:
        by_date[e["date"]].append(e)

    live = sum(1 for e in entries if e["status"] == "current")
    superseded = sum(1 for e in entries if e["status"] == "superseded")
    corrected = sum(1 for e in entries if e["corrected"] == "true")

    out = []
    out.append("# Decisions")
    out.append("")
    out.append("One file per decision. This index is **generated** by "
               "`gen-index.py` from each file's")
    out.append("frontmatter. Do not hand-edit it; regenerate it instead, so "
               "it cannot drift from the files.")
    out.append("")
    out.append("%d decisions across %d dates: **%d current**, **%d "
               "superseded**. **%d carry later corrections.**"
               % (len(entries), len(by_date), live, superseded, corrected))
    out.append("")
    out.append("## How to read this")
    out.append("")
    out.append("A `current` status does **not** mean nothing in the file was "
               "corrected. This project's")
    out.append("norm is partial supersession: a later decision retracts one "
               "named constraint while the rest")
    out.append("of the decision stands. Files marked **(corrected)** below "
               "carry a `Corrections since`")
    out.append("section, and you must read it before acting on them.")
    out.append("")
    out.append("Load only the decisions that bear on your task. Open them by "
               "path: this directory sits")
    out.append("inside a git-ignored mount, so it is invisible to "
               "ripgrep-backed search tools.")
    out.append("")

    for date in sorted(by_date):
        out.append("## %s" % date)
        out.append("")
        for e in sorted(by_date[date], key=lambda x: x["slug"]):
            flags = []
            if e["status"] == "superseded":
                flags.append("**SUPERSEDED** by `%s`" % e["superseded_by"])
            if e["corrected"] == "true":
                flags.append("**(corrected)**")
            suffix = " " + " ".join(flags) if flags else ""
            out.append("- [%s](%s)%s  " % (e["title"], e["_file"], suffix))
            out.append("  %s" % e["summary"])
        out.append("")

    target = os.path.join(d, "README.md")
    io.open(target, "w", encoding="utf-8", newline="\n").write(
        "\n".join(out).rstrip() + "\n")

    print("gen-index: wrote %s" % target)
    print("  %d decisions, %d dates, %d current, %d superseded, %d corrected"
          % (len(entries), len(by_date), live, superseded, corrected))
    return 0


if __name__ == "__main__":
    sys.exit(main())

---
date: 2026-08-09
slug: wave-b-closed-pivot-to-viewer
title: "Wave B closed; then pivot to the viewer before the remaining engine gaps"
status: current
superseded_by: null
supersedes: close-every-gap-before-viewer
summary: "Wave B complete; the viewer is built next for a visible end-to-end result, ahead of waves C and D."
corrected: false
---

## What was decided

Wave B closed the parser-identity gaps: classes and functions gained a source-root scope prefix, a scope-aware
symbol table landed, and the stitcher was changed to resolve same-source-root first. Rather than continue
straight into waves C and D, the viewer was built next to get a visible end-to-end result.

This replaces the earlier gaps-first ordering recorded in `close-every-gap-before-viewer`, whose own text
acknowledges the reversal. That entry is superseded as a whole, because sequencing was its entire substance.

## Why

The pivot was judged safe because the JSON contract is the stable seam. Later engine fixes change the numbers
inside the index, never its shape, so viewer work built against that contract does not need rework once waves C
and D land.

The headline engine result supporting the close is that the broadleaf fixture, which had previously crashed
grouping with a duplicate node identifier, now parses and groups fully.

## What this constrains

- The JSON contract is the seam. Engine changes may move the numbers in the index; they may not change its
  shape without treating that as a contract change.
- The viewer must render labels from `packagePath` plus the simple name, never the raw scoped id.

The label constraint was later reinforced, not replaced, by `engine-waves-c-and-d-closed`, which forbids path
and package-prefix heuristics for joining groups to decisions.

Do not resurrect the gaps-first ordering this entry reversed.

## Provenance

Archive: `DECISIONS.md` L798-L822, `BRAIN.md` L468-L522 (RepoHIVE-Archive, frozen)

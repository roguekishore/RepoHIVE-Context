---
date: 2026-08-23
slug: four-forward-paths-tracked-register
title: "The four forward paths get one tracked register"
status: current
superseded_by: null
supersedes: null
summary: "One tracked register is authoritative for the four post-engine paths' scope, blockers and estimates."
corrected: true
---

## What was decided

A single tracked register became the authoritative document for the four post-engine paths: component reuse,
the packaged CLI, the MCP server, and hosted deployment. It carries their scope, blockers, prerequisites and
effort estimates. The project snapshot holds only a one-line summary and a pointer to it.

## Why

The same analysis had been produced from scratch twice, both times in chat only, and both times lost at session
end. A tracked file is the fix.

Placement mattered and was got wrong first. The register was initially written into the plan directory, which
turned out to be git-ignored, so it would never have been tracked at all. It was moved to sit alongside the
other tracked working registers.

## What this constrains

- Answer path scope and blocker questions from the register, and update it, rather than re-analysing from
  scratch.
- If the register disagrees with the code, the code wins, and the register is fixed in the same change.
- Durable documentation must not be placed under the git-ignored plan directory.

## Corrections since

**This entry carries a correction to another decision.** It corrects the source-provider premise of
`live-indexing-is-a-product-requirement`: the parser reaches the filesystem in three injectable-but-unwired
places plus a required directory string, not at one injection point, so swapping the dependency collector alone
will not admit tarballs. The archive is explicit that this is a cost correction and **not** a supersession of
that entry.

**Constraint 3 of this entry is spent.** It recorded that no sequencing decision had been made across the four
paths, and that a recommendation to take component reuse first had been put forward and *not* accepted. Hours
later, `all-workstreams-run-in-parallel` closed sequencing entirely by putting every workstream into its
own worktree, running concurrently. Do not read constraint 3 as an open question.

Note on that unaccepted recommendation: its argument rested partly on an imminent external presentation rather
than on engineering grounds. It was not accepted, and the sequencing question it addressed is now closed, so
nothing turns on it. It is recorded here only so a reader does not mistake it for a live proposal with an
engineering case behind it.

Four documentation claims were corrected in the same pass. Those were consequences of the register work, not
decisions in their own right.

## Provenance

Archive: `DECISIONS.md` L500-L538, `BRAIN.md` L1052-L1113 (RepoHIVE-Archive, frozen)

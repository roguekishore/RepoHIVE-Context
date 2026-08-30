---
date: 2026-08-22
slug: public-replay-branch-topology-and-scrubbing
title: "Public replay: branch topology, and internal vocabulary stripped at the filter"
status: current
superseded_by: null
supersedes: null
summary: "Later segments replay onto real feature branches; internal vocabulary is stripped from commit messages."
corrected: false
---

## What was decided

Three things were settled about how work reaches the public repo.

Branch topology: early batches stay linear on the default branch, while every later segment is replayed onto a
real feature branch and integrated with a dated no-fast-forward merge. Branch names drop the phase-N numbering
the original branches carried.

Scrubbing: internal vocabulary is stripped from commit *messages* at the staging filter, using literal
old-to-new full-subject pairs rather than regular expressions.

Timing: one segment per calendar day, with commits spread across an ascending slot table.

## Why

Full branch topology was chosen over staying linear because the archive genuinely had those branches, which
makes the replayed topology honest rather than decorative.

The phase-N numbering was dropped because it encoded an internal milestone schedule rather than anything about
the work itself, so it is exactly the kind of internal vocabulary this entry exists to keep out of the public
history. That framing has since been removed from the project's engineering record.

Literal full-subject pairs beat regular expressions on two counts: each pair is individually reviewable, and
non-ASCII literals fail *silently* in the filter tool, so a regex that looked correct could drop a
substitution without any signal.

The ascending slot table exists so that two runs sharing a calendar date cannot produce a child commit with a
timestamp older than its parent.

## What this constrains

- Every replay branch must be merged. Commits on an unmerged branch score nothing.
- New segments follow `feat/*` naming.
- Any newly discovered internal vocabulary is added to the scrub list *before* staging is rebuilt, and the
  acceptance grep is extended to cover it.

## Provenance

Archive: `DECISIONS.md` L708-L744, `BRAIN.md` L610-L654 (RepoHIVE-Archive, frozen)

Ordering note: the archive's `DECISIONS.md` file order implies this entry predates
`agent-context-split-memory-three-files`, but the history file dates this work 20:55 and that one 21:11, and
explains the inversion: an automated stop hook prepended this entry during the later session. Ordered here by
history timestamp.

---
date: 2026-08-05
slug: close-every-gap-before-viewer
title: Close every engine gap before building the viewer
status: superseded
superseded_by: wave-b-closed-pivot-to-viewer
supersedes: null
summary: All 22 gaps were to close across four sequential branches before any viewer work began.
corrected: true
---

## What was decided

All 22 engine gaps were to be closed across four sequential branches, A parser-hardening, B parser-identity, C
engine-integrity, D engine-audit, and only then was the viewer to be built. In prose the entry also set aside
the scope and ordering of an execution-plan document that no longer exists.

## Why

The order within the plan was set by what the UI needed first, and then by how hard each gap would be to defend
under scrutiny. That moved the determinism cluster earlier and multi-module identity later.

## What this constrains

Nothing forward-binding survives. The four-wave grouping remains the historical structure of the work, and all
22 gaps did eventually close, by 2026-08-16. The sequencing this entry existed to fix is dead and must not be
resurrected: do not treat gaps-first-then-viewer as a live ordering rule.

## Corrections since

Four days later, `wave-b-closed-pivot-to-viewer` (2026-08-09) brought the viewer forward after Wave B, ahead of
waves C and D, reversing this entry's central sequencing claim. The archive source labels itself partially
superseded on that date, and the reciprocal link is recorded on both entries.

This file records the entry as `superseded` rather than `current` because the entry's substance *is* the
ordering, and the ordering was reversed. That is a judgment call taken at medium confidence: an equally
defensible reading keeps it current on the grounds that the gap-closing scope held. What survived is an
outcome, all 22 gaps closing, not a decision.

## Provenance

Archive: `DECISIONS.md` L873-L884, `BRAIN.md` L429-L466 (RepoHIVE-Archive, frozen)

Same indirect history provenance as the other 2026-08-05 entries: written to the history file twice, lost
twice, then re-recorded on 2026-08-08. The date comes from the decisions file.

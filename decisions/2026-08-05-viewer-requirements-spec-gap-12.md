---
date: 2026-08-05
slug: viewer-requirements-spec-gap-12
title: Viewer requirements spec written; Gap 12 promoted into it
status: current
superseded_by: null
supersedes: null
summary: The hierarchical-graph-viewer spec was written requirements-only; Gap 12 became Requirement 3.
corrected: false
---

## What was decided

The `hierarchical-graph-viewer` spec was written as requirements only, and approved in a single pass. Gap 12
was promoted into it as Requirement 3. Gap 1's design moved to a signal-enrichment fixes document. A planned
fixture build-out was cancelled in favour of cloning a suitable real repository when one was needed.

## Why

Promoting Gap 12 into the spec resolved that gap's open question by making group provenance a stated
requirement rather than an optional engine extra. Gap 1's design was moved only after verifying that the
existing fixes document covered gaps 3 to 22 only, a claim that had previously been asserted without being
checked.

## What this constrains

Group provenance is a viewer requirement, not an optional engine extra. That is why `regionId` and `ordinal`
later shipped as real recorded fields instead of being inferred on the client.

## Provenance

Archive: `DECISIONS.md` L904-L911, `BRAIN.md` L429-L466 (RepoHIVE-Archive, frozen)

Recorded at medium confidence, with a known provenance weakness. There is no contemporaneous history entry for
the 2026-08-05 decisions: they were written to the history file twice and lost twice to uncommitted branch
operations, then re-recorded inside the 2026-08-08 entry. The cited history range is therefore a recovery
record rather than a same-day one, and the date comes from the decisions file.

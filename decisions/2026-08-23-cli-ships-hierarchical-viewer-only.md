---
date: 2026-08-23
slug: cli-ships-hierarchical-viewer-only
title: "The CLI's shipped viewer is the hierarchical viewer only"
status: current
superseded_by: null
supersedes: null
summary: "The CLI artifact carries only the semantic-zoom viewer, built as a purpose-made single-page bundle."
corrected: true
---

## What was decided

The only viewer surface the CLI artifact must carry is the hierarchical semantic-zoom viewer. Anything else is
admissible only if it adds no weight.

The artifact is a purpose-made self-contained single-page bundle, not a static export of the vendored Next.js
application. That export plan was withdrawn, and two planned stages collapsed into one.

## Why

The scope call was the owner's, and measurement taken the same day supported it cleanly. The zoom module's only
bare-specifier imports are React and two constants, so the canvas paints itself with no heavy charting or graph
library involved. The surrounding chrome adds only an icon library, a link component and a toast library.

Because no framework or heavy visualization dependency is actually needed to ship that surface, exporting the
whole vendored application would drag in weight the artifact has no use for. A purpose-made bundle is the
smaller and more honest shape.

## What this constrains

- Do not static-export the vendored Next.js app for the CLI. That plan is withdrawn.
- Build a self-contained single-page artifact instead.

## Corrections since

**This entry itself retracts two claims made earlier the same day.** It withdraws the proposed
static-export-the-vendored-app plan, and it retracts an 18:25 claim that the component-reuse path's subtractive
pass was upstream of the CLI's shippable viewer. That dependency only ever held while the CLI was to ship the
whole vendored application, which it no longer is.

**Constraint 4 of this entry is spent.** It recorded the choice of bundler as an open decision. That was closed
the same evening: `cli-requirements-spec-unblocked` picked a specific single-file bundler plugin, verified
against the registry before adoption, and `steering-tool-lists-are-extensible` removed the reading of a
do-not-reintroduce line that had made adding a bundler look prohibited. Do not treat the bundler as open.

## Provenance

Archive: `DECISIONS.md` L430-L460, `BRAIN.md` L1186-L1235 (RepoHIVE-Archive, frozen)

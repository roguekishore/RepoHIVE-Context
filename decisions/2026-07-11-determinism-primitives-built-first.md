---
date: 2026-07-11
slug: determinism-primitives-built-first
title: Determinism primitives are built first, always
status: current
superseded_by: null
supersedes: null
summary: Canonical ordering and content-addressed stable ids were built before any algorithm stage.
corrected: true
---

## What was decided

Phase-2 implementation began with canonical ordering, stable stringify and content-addressed group ids, before
any algorithm stage existed. In the same entry, both engine packages' test runners were scoped to compiled
`dist/` tests for Node-version compatibility.

## Why

Every later stage depends on those primitives, so adding determinism afterwards means rewriting everything
built on top of it. Determinism is treated as foundational rather than as a property to be achieved later.

## What this constrains

Every stage sits on canonical order and stable ids. This is the root of the hard determinism constraint that
later decisions repeatedly invoke: a prefetch design that would let read-completion order reach the graph is
forbidden, and the viewer's layout must be seeded and stable. Retrofitting determinism would mean rewriting
everything above it.

## Corrections since

The test-runner clause proved defective. Scoping both engine runners to compiled `dist/` tests is recorded as
the origin of the Node-version test-runner defect found on 2026-08-22 by `npm-test-not-a-green-gate`: neither
runner form works on both Node 20 and Node 21+, so no claim that the suite is green may be made from a root
`npm test` run. Verification instead uses an explicit file list compared against the recorded known-failure
list.

The determinism decision itself stands unchanged.

## Provenance

Archive: `DECISIONS.md` L922-L929, `BRAIN.md` L318-L330 (RepoHIVE-Archive, frozen)

---
date: 2026-08-05
slug: commit-granularity-is-rollback-guarantee
title: Commit granularity is a rollback guarantee
status: current
superseded_by: null
supersedes: null
summary: One commit per observable sub-behaviour, each independently building and passing, replacing one-per-gap.
corrected: true
---

## What was decided

Commit granularity moved to one commit per observable sub-behaviour, three to seven per gap, each independently
building and passing. This replaced the earlier one-commit-per-gap rule.

## Why

A commit that does not build and pass is not a rollback point, so coarse commits defeat the purpose of having
them. A gotcha was recorded at the same time because it had already bitten: `graph.json` and the index
directory are git-ignored, so reverting code does not restore the artifacts that matched it.

## What this constrains

Build plus the full suite before every commit. Reverting code does not restore git-ignored artifacts that
matched it, so a rollback of code is not a rollback of generated output. The rule was restated and reused by
`repo-split-archive-plus-scrubbed-replay` (2026-08-08) as the public replay's commit granularity.

## Corrections since

**The "full suite before every commit" gate was materially undermined on 2026-08-22** by
`npm-test-not-a-green-gate`, which found that a root `npm test` run was never a valid green gate: neither
test-runner form works on both Node 20 and Node 21+, so whether the engine tests ran at all depended on which
Node version the machine happened to have. The rule itself stands, but every historical claim of having
satisfied it is unreliable. To satisfy the gate now, verify the engine with an explicit file list and compare
against the recorded known-failure list; a change is clean if it does not add to that list.

## Provenance

Archive: `DECISIONS.md` L862-L872, `BRAIN.md` L401-L428 (RepoHIVE-Archive, frozen)

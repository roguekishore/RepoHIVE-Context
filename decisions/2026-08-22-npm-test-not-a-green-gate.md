---
date: 2026-08-22
slug: npm-test-not-a-green-gate
title: "npm test is not a valid green gate until the engine runner is version-independent"
status: current
superseded_by: null
supersedes: null
summary: "Neither test-runner form works on both Node 20 and 21+, so every historical green claim was unreliable."
corrected: false
---

## What was decided

No claim that the suite is green may be made from a root `npm test` run. Until the engine test runner is
version-independent, verification is done by passing an explicit file list and comparing the result against the
recorded known-failure list. A change is clean if it does not add to that list.

## Why

Root `npm test` exits non-zero, and the engine packages' tests do not run at all on the development machine.
The mechanism is precise and worth keeping:

- The glob form of the runner depends on Node 21+ expanding the glob. `cmd.exe` does not expand it either, so
  on Node 20 the runner finds nothing and runs nothing, while still looking like it ran.
- The directory form it replaced does run on Node 20, but on Node 21+ it silently resolves to a single index
  file and reports one passing test.

Neither form is correct on both versions. So every historical claim of having been green before a commit
depended on which Node version the machine happened to have at the time, which makes those claims unreliable
rather than merely unverified.

Three named failures are pre-existing and sit outside engine logic.

## What this constrains

- Do not report the suite as green on the strength of a root `npm test` run.
- Verify the engine with an explicit file list, checked against the recorded known-failure list.
- Two earlier records are affected by this finding:
  - The "suite 354 green" figure in `engine-waves-c-and-d-closed` is retracted. It covered three of six test
    workspaces and was captured on a different Node version.
  - The build-and-test-before-every-commit gate in `commit-granularity-is-rollback-guarantee` still stands as a
    rule, but historical claims of having satisfied it are unreliable.

## Provenance

Archive: `DECISIONS.md` L678-L707, `BRAIN.md` L699-L709 (RepoHIVE-Archive, frozen). The history citation is the
measurement block inside the 21:11 session entry rather than a separate entry of its own.

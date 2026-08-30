---
date: 2026-08-16
slug: engine-waves-c-and-d-closed
title: "Engine waves C and D closed, plus the viewer finish"
status: current
superseded_by: null
supersedes: null
summary: "All 22 gaps closed; the group-to-region package-prefix heuristic was removed in favour of real provenance."
corrected: true
---

## What was decided

Waves C (engine-integrity) and D (engine-audit) completed, closing all 22 engine gaps. Determinism held.
Digests were recaptured because metadata gained a resolved-configuration block and nodes gained region
provenance, which are additive contract changes rather than a determinism regression.

The viewer finish removed the group-to-region package-prefix heuristic entirely. Real `regionId` and `ordinal`
fields on group nodes, plus `groupIds` on each decision, now drive the decision badge, the summary, the audit
cross-link and the group label. This was verified against the committed fixture at both boundary extremes.

## Why

Inferring a group's region from its package path was a guess that happened to work on the fixtures. Recording
provenance as real fields makes the join exact, which is why group provenance was made a stated viewer
requirement rather than an optional engine extra.

## What this constrains

- Consumers join groups to decisions through `regionId`, `ordinal` and `groupIds`. No path or package-prefix
  heuristic may be reintroduced for that purpose.
- A residual promotion hazard is recorded as inherent to the design, not as an open defect: the change runs as
  five same-directory renames, and a failure between them can still leave a mixture on disk.

## Corrections since

The "suite 354 green" figure recorded in this entry is retracted by `npm-test-not-a-green-gate`. That figure
covered three of six test workspaces and was captured on a different Node version, so it is not evidence that
the suite was green. Do not quote it. Verify the engine with an explicit file list compared against the
recorded known-failure list instead.

Everything else here stands. The constraint about joining through recorded provenance is unaffected and still
binds.

## Provenance

Archive: `DECISIONS.md` L771-L797, `BRAIN.md` L525-L563, L567-L606 (RepoHIVE-Archive, frozen)

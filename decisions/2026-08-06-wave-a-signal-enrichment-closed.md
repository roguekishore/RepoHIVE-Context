---
date: 2026-08-06
slug: wave-a-signal-enrichment-closed
title: Wave A closed; signal enrichment made the adaptive branch fire on real Java
status: current
superseded_by: null
supersedes: null
summary: Gaps 16, 1a and 1c resolved, taking vantage from preserve 0/20 to 10/10 as edges went 128 to 341.
corrected: false
---

## What was decided

Wave A closed. Gaps 16, 1a and 1c were resolved in 11 granular commits: strength-aware degenerate guards that
prevent a singleton explosion on zero-weight edges, type-use edge extraction to populate the shared-type
signal, and same-package simple-name resolution to create intra-package edges.

## Why

The headline result is why this matters. The 158-file vantage fixture re-parsed to 341 edges from 128, and
moved to preserve 10 / reconstruct 10 from 0/20. Before this work the preserve branch never fired on real Java,
which meant the project's central contribution was not demonstrable. Two Tree-Sitter grammar traps were caught
during testing.

## What this constrains

The preserve branch only fires once parser signals are populated. Tree-Sitter grammar assumptions must be
verified empirically rather than assumed.

This result is also the evidence base for a later structural finding, recorded 2026-08-22: the
preserve-vs-reconstruct split is partly a function of parser signal volume, not only of repository quality, so
enriching the parser shifts the decision boundary. That was recorded as a calibration risk to be aware of, not
as a defect, and it does not supersede anything decided here.

## Provenance

Archive: `DECISIONS.md` L846-L861, `BRAIN.md` L401-L428 (RepoHIVE-Archive, frozen)

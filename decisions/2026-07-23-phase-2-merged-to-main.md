---
date: 2026-07-23
slug: phase-2-merged-to-main
title: Phase 2 grouping engine merged to main
status: current
superseded_by: null
supersedes: null
summary: The grouping engine landed one commit per spec task, with 79 core tests covering 33 properties.
corrected: true
---

## What was decided

This is an outcome record rather than a forward-binding choice. `phase-2-core` merged `--no-ff`, landing the
grouping engine as one commit per spec task with tests alongside, recorded at the time as 79 core tests
covering 33 correctness properties, 181 tests in total.

The pipeline shipped in dependency order: deterministic primitives, the ingest gate, dependency strengths,
region identification, structural-quality assessment, the seeded-Louvain community seam, adaptive
preserve-vs-reconstruct construction, balanced hierarchy assembly, metadata, whole-pipeline determinism, the
five-file index serialize and parse pair, blast radius, and the orchestrator with its `group` CLI.

## Why

Byte-identical SHA-256 output was proven across repeated runs and across shuffled-input runs. That is the
determinism evidence for the engine at its completion point.

## What this constrains

Marks the engine's completion point and its determinism evidence. From here, the five-file index set is the
contract seam that downstream surfaces consume.

## Corrections since

The test figures here are historical, not a current suite count. They were overtaken as later waves closed,
through 257, 297 and 334, and then by the corrected per-workspace figures of 2026-08-22. Separately,
`npm-test-not-a-green-gate` (2026-08-22) found that a root `npm test` run was never a valid green gate on this
project, so any suite total from this era should be read as what was reported at the time rather than as a
verified figure. As a record of this merge and of its byte-identical determinism result, the entry stands.

## Provenance

Archive: `DECISIONS.md` L912-L921, `BRAIN.md` L390-L400 (RepoHIVE-Archive, frozen)

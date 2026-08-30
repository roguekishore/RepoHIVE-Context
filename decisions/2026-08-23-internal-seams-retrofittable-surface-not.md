---
date: 2026-08-23
slug: internal-seams-retrofittable-surface-not
title: Internal seams are retrofittable; the published CLI surface is not
status: current
superseded_by: null
supersedes: null
summary: Only orchestration is a CLI prerequisite; the other three seams retrofit safely behind existing functions.
corrected: false
---

## What was decided

Of the four foundation seams, only orchestration is a genuine prerequisite for the CLI, and the CLI contains
that layer naturally because the index command *is* the parse-then-group orchestration. The other three, the
source provider, the storage interface, and content-addressed snapshot ids, are all safely addable later. The
CLI is therefore not blocked on seam work. It is blocked on the artifact layout and the CLI contract. The seam
design still gets a proper spec, written concurrently rather than first.

## Why

Putting an interface behind an existing function is backwards-compatible as long as the default behaviour is
preserved, and that is already the house pattern in this codebase: a deps parameter defaulting to a real
filesystem implementation, used in two places. So the internal architecture stays cheap to change.

The published surface does not have that property. Once anyone writes automation against the CLI, changing the
on-disk layout, the command names, the flag names, the JSON output shape, or the exit codes is a major version
bump and a broken build for that person. The inversion is the durable content of this decision: the thing that
cannot be retrofitted is the surface, not the architecture behind it.

## What this constrains

- Do not block the CLI on seam work. Block it on the artifact layout and the CLI contract.
- The on-disk layout, command names, flag names, JSON output shape, and exit codes must be right before the
  first publish.
- Adding an interface behind an existing function is acceptable later work, provided the existing default is
  preserved.

This workstream was paused mid-planning by `viewer-handed-to-fable-workstreams-held`. The pause is a hold, not a
cancellation: this decision and its constraints still stand, and the work resumes on an explicit owner call.

## Provenance

Archive: `DECISIONS.md` L402-L429, `BRAIN.md` L1265-L1314 (RepoHIVE-Archive, frozen)
